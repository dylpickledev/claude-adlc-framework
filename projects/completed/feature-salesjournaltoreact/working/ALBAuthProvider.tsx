// GraniteRock Sales Journal - ALB Authentication Provider
// Handles SSO authentication via Application Load Balancer + IAM Identity Center (OIDC)
// Production-ready implementation with comprehensive error handling

import React, { useEffect, useState } from 'react';
import styled from 'styled-components';

interface ALBUser {
  email: string;
  name: string;
  sub: string;
  groups?: string[];
}

interface ALBAuthProviderProps {
  children: (user: ALBUser | null, signOut: () => void) => React.ReactNode;
}

const LoadingContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #0f4c38 0%, #2d8a5f 100%);
  color: white;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
`;

const Logo = styled.div`
  font-size: 4rem;
  margin-bottom: 24px;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
`;

const Title = styled.h1`
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 8px;
  text-align: center;
`;

const Subtitle = styled.p`
  font-size: 1rem;
  opacity: 0.9;
  margin-bottom: 32px;
  text-align: center;
  max-width: 500px;
  padding: 0 20px;
`;

const ErrorBox = styled.div`
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.5);
  border-radius: 8px;
  padding: 16px 24px;
  margin-top: 24px;
  max-width: 500px;
  text-align: left;

  h3 {
    margin: 0 0 12px 0;
    font-size: 1.125rem;
  }

  p {
    margin: 0;
    font-size: 0.875rem;
    opacity: 0.9;
  }

  details {
    margin-top: 12px;
    font-size: 0.75rem;
    opacity: 0.8;
  }
`;

const Spinner = styled.div`
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
`;

const RefreshButton = styled.button`
  background: white;
  color: #0f4c38;
  padding: 12px 32px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 16px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }

  &:active {
    transform: translateY(0);
  }
`;

/**
 * Parse JWT token payload without validation
 * ALB already validated the token signature, we just need to extract claims
 */
const parseJWT = (token: string): any => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('JWT parsing error:', error);
    throw new Error('Invalid JWT format');
  }
};

/**
 * Read ALB authentication headers from meta tags
 * ALB injects these via nginx configuration
 */
const readALBHeaders = (): { identity: string | null; data: string | null } => {
  const identityMeta = document.querySelector('meta[name="x-amzn-oidc-identity"]');
  const dataMeta = document.querySelector('meta[name="x-amzn-oidc-data"]');

  return {
    identity: identityMeta?.getAttribute('content') || null,
    data: dataMeta?.getAttribute('content') || null,
  };
};

export const ALBAuthProvider: React.FC<ALBAuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<ALBUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [debugInfo, setDebugInfo] = useState<string>('');

  useEffect(() => {
    authenticateUser();
  }, []);

  const authenticateUser = async () => {
    try {
      setLoading(true);
      setError(null);

      // Read ALB-injected headers from meta tags
      const { identity, data } = readALBHeaders();

      // Debug information for troubleshooting
      const debug = {
        hasIdentity: !!identity,
        hasData: !!data,
        identityLength: identity?.length || 0,
        dataLength: data?.length || 0,
        metaTagsPresent: {
          identity: !!document.querySelector('meta[name="x-amzn-oidc-identity"]'),
          data: !!document.querySelector('meta[name="x-amzn-oidc-data"]'),
        },
      };
      setDebugInfo(JSON.stringify(debug, null, 2));

      // Validate required headers exist
      if (!data) {
        throw new Error(
          'ALB authentication headers not found. This application must be accessed through the Application Load Balancer.'
        );
      }

      // Parse JWT to extract user claims
      const payload = parseJWT(data);

      // Validate required claims
      if (!payload.email) {
        throw new Error('User email not found in authentication token');
      }

      // Extract user information from JWT claims
      const authenticatedUser: ALBUser = {
        email: payload.email,
        name: payload.name || payload.email.split('@')[0],
        sub: payload.sub,
        groups: payload['cognito:groups'] || [],
      };

      console.log('ALB authentication successful:', {
        email: authenticatedUser.email,
        name: authenticatedUser.name,
        groups: authenticatedUser.groups,
      });

      setUser(authenticatedUser);
      setLoading(false);
    } catch (err: any) {
      console.error('ALB authentication error:', err);
      setError(err.message || 'Authentication failed');
      setUser(null);
      setLoading(false);
    }
  };

  const signOut = () => {
    // Redirect to ALB logout endpoint
    // ALB will clear the session cookie and redirect back to IAM Identity Center
    window.location.href = '/logout';
  };

  const handleRefresh = () => {
    window.location.reload();
  };

  // Loading state
  if (loading) {
    return (
      <LoadingContainer>
        <Spinner />
        <Title>GraniteRock Sales Journal</Title>
        <Subtitle>Verifying your authentication...</Subtitle>
      </LoadingContainer>
    );
  }

  // Error state
  if (error || !user) {
    return (
      <LoadingContainer>
        <Logo>🏔️</Logo>
        <Title>Authentication Required</Title>
        <Subtitle>
          You must be authenticated through the GraniteRock SSO portal to access this application.
        </Subtitle>
        <ErrorBox>
          <h3>⚠️ Authentication Error</h3>
          <p>{error || 'Unable to verify your identity'}</p>
          <details>
            <summary>Technical Details</summary>
            <pre>{debugInfo}</pre>
          </details>
        </ErrorBox>
        <RefreshButton onClick={handleRefresh}>
          🔄 Refresh Page
        </RefreshButton>
      </LoadingContainer>
    );
  }

  // Authenticated - render application
  return <>{children(user, signOut)}</>;
};

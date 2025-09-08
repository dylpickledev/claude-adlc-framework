# Repository Workspace

This directory contains cloned or symlinked repositories for the D&A Agent Hub.

## Automatic Repository Management

The `setup.sh` script automatically clones **ALL** repositories and knowledge sources configured in `config/repositories.json`:

### Code Repositories
- **dbt_cloud**: Main dbt transformation project (branch: dbt_dw)
- **dbt_errors_to_issues**: dbt error reporting automation (branch: main)
- **roy_kent**: Roy Kent coaching system (branch: master)  
- **sherlock**: Sherlock investigation system (branch: main)
- **orchestra**: Orchestra workflow orchestration system (branch: main)
- **postgres_pipelines**: PostgreSQL data pipeline configurations (branch: main)
- **dbt_postgres**: dbt transformations for PostgreSQL (branch: main)

### Knowledge Sources
- **da_team_documentation**: Data & Analytics team documentation (branch: main)

## Repository Sources

All repositories are cloned from the `graniterock` GitHub organization using HTTPS. If a GitHub personal access token is configured in `.env`, it will be used for authenticated access to private repositories.

## Version Control

- **This folder structure** is included in da-agent-hub version control
- **Repository contents** are excluded via `.gitignore` - each repository maintains its own version control
- Cloned repositories will use their configured default branches
- Local changes to cloned repositories are not tracked by da-agent-hub

## Clone-Only Operation

All repositories are cloned directly from the configured sources. No symlink fallback is provided - this is your primary workspace for data operations.

## Manual Management

To manually update repositories:

```bash
# Update all repositories
cd repos/dbt_cloud && git pull origin dbt_dw
cd ../sherlock && git pull origin main
# etc.

# Or re-run setup to update all
./setup.sh
```

This workspace organization allows expert agents to access relevant codebases while maintaining clean separation of concerns and version control boundaries.
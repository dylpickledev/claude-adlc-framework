# Workspace Directory

This directory contains symlinks to your actual repositories.

## Adding Repositories

To add a repository to your workspace:

```bash
ln -s /path/to/your/repo workspace/repo-name
```

## Recommended Structure

- `dbt/` - dbt project repository
- `dlthub/` - dlthub project repository
- `orchestration/` - Orchestra/Airflow DAGs
- `tableau/` - Tableau workbooks and scripts
- `docs/` - Documentation repository

## Customization

Edit `developer/workspace-config.sh` to automate your specific symlink setup.

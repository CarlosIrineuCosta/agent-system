# Claude Commands Directory

This directory contains Claude slash commands for the agent-system-standalone project.

## Main Commands

The following commands are ready to use:

- **`server.md`** - Server management and control
- **`dev.md`** - Local development environment setup
- **`check.md`** - Quality assurance and testing
- **`start.md`** - Session initialization and setup
- **`end.md`** - Session cleanup and summary
- **`ui.md`** - Frontend UI development and design
- **`api.md`** - Backend API development and integration

## Deployment Commands

### Configuration Required

The following commands in the `deployment/` subdirectory **require adaptation** before use:

- **`deployment/deploy.md`** - Basic deployment pipeline
- **`deployment/deploy-enhanced.md`** - Enhanced deployment with safety checks

### What Needs Configuration

For the deployment commands, you must update:

1. **Server Addresses**
   - Current: `83.172.136.127` (EDIS Swiss VPS)
   - Change to: Your target server IP

2. **Domain Names**
   - Current: `lumenphotos.com`
   - Change to: Your domain

3. **SSH Credentials**
   - Current: `root@83.172.136.127`
   - Change to: Your SSH user and server

4. **File Paths**
   - Current: `/opt/lumen-backend/` and `/opt/lumen-frontend/`
   - Change to: Your deployment paths

5. **Database Configuration**
   - Current: `lumen_user` and `lumen_db`
   - Change to: Your database settings

6. **Service Names**
   - Current: `lumen-backend`
   - Change to: Your service name

### Safety Features

The deployment commands include:

- Automated backups before deployment
- Disk space validation
- Health checks after deployment
- Rollback capability
- Comprehensive logging

## Usage

To use any command, type:
```
/command-name
```

For commands with arguments:
```
/command-name argument1 argument2
```

## Important Notes

- Always test deployment commands in a staging environment first
- Keep backups before running deployment commands
- Monitor disk space on target servers
- Ensure SSH keys are properly configured for automated deployment
- Review each command's safety features before use
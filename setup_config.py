#!/usr/bin/env python3
"""
Setup Configuration for SMM MCP Server
Interactive script to help users configure their SMM MCP Server
"""

import os
import sys
from pathlib import Path

def setup_config():
    """Interactive configuration setup"""
    print("🔧 SMM MCP Server Configuration Setup")
    print("=" * 50)
    print()
    
    # Check if .env already exists
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("Configuration setup cancelled.")
            return
    
    print("Please provide your SMM configuration details:")
    print()
    
    # Get configuration type
    print("1. CDP SMM deployment (via Apache Knox)")
    print("2. Standalone SMM deployment")
    config_type = input("Select configuration type (1 or 2): ").strip()
    
    config_lines = []
    
    if config_type == "1":
        print("\n📡 CDP SMM Configuration (Apache Knox)")
        print("-" * 40)
        
        gateway_url = input("Knox Gateway URL (e.g., https://your-knox-gateway:8444/gateway/smm): ").strip()
        if not gateway_url:
            gateway_url = "https://your-knox-gateway:8444/gateway/smm"
        
        auth_method = input("Authentication method (1=Username/Password, 2=JWT Token): ").strip()
        
        if auth_method == "2":
            token = input("Knox JWT Token: ").strip()
            config_lines.extend([
                f"KNOX_GATEWAY_URL={gateway_url}",
                f"KNOX_TOKEN={token}",
                ""
            ])
        else:
            username = input("Knox Username: ").strip()
            password = input("Knox Password: ").strip()
            config_lines.extend([
                f"KNOX_GATEWAY_URL={gateway_url}",
                f"KNOX_USER={username}",
                f"KNOX_PASSWORD={password}",
                ""
            ])
    
    elif config_type == "2":
        print("\n🖥️  Standalone SMM Configuration")
        print("-" * 40)
        
        api_base = input("SMM API Base URL (e.g., http://localhost:8080/api/v2): ").strip()
        if not api_base:
            api_base = "http://localhost:8080/api/v2"
        
        username = input("SMM Username: ").strip()
        password = input("SMM Password: ").strip()
        
        config_lines.extend([
            f"SMM_API_BASE={api_base}",
            f"SMM_USER={username}",
            f"SMM_PASSWORD={password}",
            ""
        ])
    
    else:
        print("❌ Invalid selection. Configuration setup cancelled.")
        return
    
    # Add common configuration
    readonly = input("Enable read-only mode? (Y/n): ").strip().lower()
    if readonly == 'n':
        config_lines.append("SMM_READONLY=false")
    else:
        config_lines.append("SMM_READONLY=true")
    
    config_lines.extend([
        "KNOX_VERIFY_SSL=true",
        "HTTP_TIMEOUT_SECONDS=30",
        "MCP_TRANSPORT=stdio"
    ])
    
    # Write .env file
    try:
        with open(".env", "w") as f:
            f.write("\n".join(config_lines))
        print(f"\n✅ Configuration saved to .env")
        print("You can now run the MCP server with your configuration.")
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")
        return
    
    print("\n📋 Next Steps:")
    print("1. Review your .env file to ensure all values are correct")
    print("2. Configure Claude Desktop with the MCP server")
    print("3. Restart Claude Desktop")
    print("4. Start using the SMM MCP Server!")

def main():
    """Main function"""
    try:
        setup_config()
    except KeyboardInterrupt:
        print("\n\nConfiguration setup cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any

from telethon import TelegramClient

from utils import *

def load_config() -> Dict[str, Any]:
    """Load and validate configuration."""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.loads(f.read())
        
        required_fields = ['accounts', 'api_id', 'api_hash']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required config field: {field}")
        
        return config
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        sys.exit(1)

def initialize_session(phone: str, session_path: Path, api_id: int, api_hash: str) -> bool:
    """Initialize a single Telegram session."""
    try:
        client = TelegramClient(
            str(session_path / phone),
            api_id,
            api_hash
        )
        
        client.start()
        
        if client.is_user_authorized():
            logging.info(f"Login successful for {phone}")
            return True
        else:
            logging.warning(f"Login failed for {phone}")
            return False
            
    except Exception as e:
        logging.error(f"Error initializing session for {phone}: {e}")
        return False
    finally:
        if 'client' in locals():
            client.disconnect()

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Load configuration
    config = load_config()
    
    # Setup paths
    session_path = Path('session')
    session_path.mkdir(exist_ok=True)
    
    # Initialize sessions
    success_count = 0
    for phone in config['accounts']:
        if initialize_session(
            phone,
            session_path,
            int(config['api_id']),
            config['api_hash']
        ):
            success_count += 1
    
    logging.info(f"Successfully initialized {success_count} out of {len(config['accounts'])} sessions")

if __name__ == "__main__":
    main()

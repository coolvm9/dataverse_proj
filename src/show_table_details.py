#!/usr/bin/env python3
"""
Show Dataverse table details and schema information.

This script displays comprehensive table information including
attributes, data types, and schema details from Microsoft Dataverse.
"""

import json
from dataverse_client import DataverseClient

def main():
    print("Dataverse Table Details")
    print("=" * 30)
    
    try:
        client = DataverseClient()
        
        if not client.test_connection():
            print("❌ Failed to connect to Dataverse")
            return
        
        print("✅ Connected to Dataverse successfully!")
        
        table_name = input("\nEnter table name to retrieve schema (e.g., 'account', 'contact'): ").strip()
        
        if not table_name:
            print("Using 'account' as default table name")
            table_name = "account"
        
        print(f"\n📋 Retrieving schema for table: {table_name}")
        
        try:
            schema = client.get_table_schema(table_name)
            
            print(f"\n✅ Schema retrieved for table: {schema.get('LogicalName')}")
            print(f"Display Name: {schema.get('DisplayName', {}).get('UserLocalizedLabel', {}).get('Label', 'N/A')}")
            print(f"Schema Name: {schema.get('SchemaName')}")
            print(f"Entity Set Name: {schema.get('EntitySetName')}")
            
            attributes = schema.get('Attributes', [])
            print(f"\n📊 Found {len(attributes)} attributes:")
            
            for attr in attributes[:10]:  # Show first 10 attributes
                attr_name = attr.get('LogicalName')
                attr_type = attr.get('AttributeType')
                display_name = attr.get('DisplayName', {}).get('UserLocalizedLabel', {}).get('Label', 'N/A')
                is_primary = attr.get('IsPrimaryId', False)
                primary_indicator = " (PRIMARY KEY)" if is_primary else ""
                
                print(f"  - {attr_name}: {attr_type} - {display_name}{primary_indicator}")
            
            if len(attributes) > 10:
                print(f"  ... and {len(attributes) - 10} more attributes")
            
            print(f"\n🔍 Getting detailed attributes for table: {table_name}")
            detailed_attrs = client.get_table_attributes(table_name)
            
            print(f"\n📝 Detailed attribute information (first 5):")
            for attr in detailed_attrs[:5]:
                print(f"  - {attr.get('LogicalName')}:")
                print(f"    Type: {attr.get('AttributeType')}")
                print(f"    Schema Name: {attr.get('SchemaName')}")
                print(f"    Can Create: {attr.get('IsValidForCreate')}")
                print(f"    Can Update: {attr.get('IsValidForUpdate')}")
                print()
                
        except Exception as e:
            print(f"❌ Error retrieving schema for table '{table_name}': {e}")
            print("💡 Make sure the table name is correct and accessible")
        
        save_to_file = input("Save schema to JSON file? (y/N): ").strip().lower()
        if save_to_file == 'y':
            filename = f"{table_name}_schema.json"
            with open(filename, 'w') as f:
                json.dump(schema, f, indent=2)
            print(f"💾 Schema saved to {filename}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
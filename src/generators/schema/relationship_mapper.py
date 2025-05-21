"""Schema relationship mapping utility."""

import os
import json
from typing import Dict, List, Any, Optional

from microgenesis.logging import get_logger

logger = get_logger()


class SchemaRelationshipMapper:
    """Utility for mapping relationships between entities."""
    
    def __init__(self, mapping_file: Optional[str] = None):
        """Initialize the schema relationship mapper.
        
        Args:
            mapping_file: Path to the schema mapping file (optional)
        """
        self.logger = get_logger()
        self.relationships = {}
        
        if mapping_file:
            self._load_mapping_file(mapping_file)
    
    def _load_mapping_file(self, mapping_file: str) -> None:
        """Load relationship mappings from a file.
        
        Args:
            mapping_file: Path to the schema mapping file
        """
        try:
            with open(mapping_file, 'r') as f:
                self.relationships = json.load(f)
            self.logger.info(f"Loaded schema relationships from {mapping_file}")
        except Exception as e:
            self.logger.error(f"Failed to load schema mapping file: {e}")
            self.relationships = {}
    
    def enrich_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich entity definitions with relationship information.
        
        Args:
            entities: List of entity definitions
            
        Returns:
            List[Dict[str, Any]]: Enriched entity definitions with relationships
        """
        # If no relationships defined, return original entities
        if not self.relationships:
            return entities
        
        # Create a map of entity names for quick lookup
        entity_map = {entity["name"]: entity for entity in entities}
        enriched_entities = []
        
        # Process each entity and add relationship fields
        for entity_name, entity in entity_map.items():
            # Look for relationships where this entity is the source
            if entity_name in self.relationships:
                entity_relationships = self.relationships[entity_name]
                
                # Process each relationship
                for relationship in entity_relationships:
                    target_entity = relationship.get("target")
                    relationship_type = relationship.get("type", "one-to-many")
                    field_name = relationship.get("fieldName", target_entity.lower())
                    
                    # Skip if target entity doesn't exist
                    if target_entity not in entity_map:
                        self.logger.warning(f"Target entity {target_entity} not found for relationship in {entity_name}")
                        continue
                    
                    # Get target ID field type
                    target_entity_def = entity_map[target_entity]
                    target_id_field = next((f for f in target_entity_def.get("fields", []) if f.get("name") == "id"), None)
                    target_id_type = target_id_field.get("type", "Long") if target_id_field else "Long"
                    
                    # Add field based on relationship type
                    if relationship_type == "one-to-one":
                        field = {
                            "name": field_name,
                            "type": target_entity,
                            "annotations": [f"@OneToOne", "@JoinColumn(name = \"{field_name}_id\")"]
                        }
                        entity.setdefault("fields", []).append(field)
                    
                    elif relationship_type == "many-to-one":
                        field = {
                            "name": field_name,
                            "type": target_entity,
                            "annotations": [f"@ManyToOne", "@JoinColumn(name = \"{field_name}_id\")"]
                        }
                        entity.setdefault("fields", []).append(field)
                    
                    elif relationship_type == "one-to-many":
                        field = {
                            "name": f"{field_name}List",
                            "type": f"List<{target_entity}>",
                            "annotations": [f"@OneToMany(mappedBy = \"{entity_name.lower()}\")"]
                        }
                        entity.setdefault("fields", []).append(field)
                    
                    elif relationship_type == "many-to-many":
                        field = {
                            "name": f"{field_name}List",
                            "type": f"List<{target_entity}>",
                            "annotations": [
                                f"@ManyToMany",
                                f"@JoinTable(name = \"{entity_name.lower()}_{target_entity.lower()}\", " +
                                f"joinColumns = @JoinColumn(name = \"{entity_name.lower()}_id\"), " +
                                f"inverseJoinColumns = @JoinColumn(name = \"{target_entity.lower()}_id\"))"
                            ]
                        }
                        entity.setdefault("fields", []).append(field)
            
            # Add to enriched entities
            enriched_entities.append(entity)
        
        return enriched_entities
    
    def generate_mapping_file(self, entities: List[Dict[str, Any]], output_file: str) -> None:
        """Generate a template mapping file based on the provided entities.
        
        Args:
            entities: List of entity definitions
            output_file: Path to the output mapping file
        """
        relationships = {}
        
        # For each entity, create a template relationship with every other entity
        for source_entity in entities:
            source_name = source_entity["name"]
            relationships[source_name] = []
            
            for target_entity in entities:
                target_name = target_entity["name"]
                if target_name != source_name:
                    # Create a template relationship entry
                    relationship = {
                        "target": target_name,
                        "type": "one-to-many",  # Default type
                        "fieldName": target_name[0].lower() + target_name[1:],
                        "bidirectional": False,
                        "cascade": ["ALL"],
                        "fetch": "LAZY",
                        "optional": True
                    }
                    relationships[source_name].append(relationship)
        
        # Write to file
        try:
            with open(output_file, 'w') as f:
                json.dump(relationships, f, indent=2)
            self.logger.info(f"Generated schema relationship template at {output_file}")
        except Exception as e:
            self.logger.error(f"Failed to generate schema mapping file: {e}")
    
    def analyze_entity_fields(self, entities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze entity fields to detect potential relationships.
        
        This method looks for fields that might represent relationships based on naming conventions.
        
        Args:
            entities: List of entity definitions
            
        Returns:
            Dict[str, List[Dict[str, Any]]]: Detected relationship mappings
        """
        entity_names = {entity["name"] for entity in entities}
        detected_relationships = {}
        
        # For each entity, look for fields that might reference other entities
        for entity in entities:
            entity_name = entity["name"]
            detected_relationships[entity_name] = []
            
            for field in entity.get("fields", []):
                field_name = field["name"]
                field_type = field["type"]
                
                # Remove List<> wrapper if present
                if field_type.startswith("List<") and field_type.endswith(">"):
                    inner_type = field_type[5:-1]  # Extract type inside List<>
                    
                    # Check if the inner type matches an entity name
                    if inner_type in entity_names:
                        relationship = {
                            "target": inner_type,
                            "type": "one-to-many",
                            "fieldName": field_name,
                            "bidirectional": False
                        }
                        detected_relationships[entity_name].append(relationship)
                
                # Check if field type directly matches an entity name
                elif field_type in entity_names:
                    relationship = {
                        "target": field_type,
                        "type": "many-to-one",
                        "fieldName": field_name,
                        "bidirectional": False
                    }
                    detected_relationships[entity_name].append(relationship)
                
                # Check for ID fields that might indicate a relationship
                elif field_name.endswith("Id") and not field_name == "id":
                    # Extract potential entity name from field name
                    potential_entity = field_name[0].upper() + field_name[1:-2]
                    if potential_entity in entity_names:
                        relationship = {
                            "target": potential_entity,
                            "type": "many-to-one",
                            "fieldName": field_name[:-2],  # Remove 'Id' suffix
                            "bidirectional": False
                        }
                        detected_relationships[entity_name].append(relationship)
        
        return {k: v for k, v in detected_relationships.items() if v}

"""Unit tests for Schema Relationship Mapper."""

import unittest
import tempfile
import os
import json
from microgenesis.generators.schema.relationship_mapper import SchemaRelationshipMapper


class TestSchemaRelationshipMapper(unittest.TestCase):
    """Test cases for Schema Relationship Mapper."""
    
    def setUp(self):
        """Set up the test environment."""
        self.mapper = SchemaRelationshipMapper()
        self.temp_dir = tempfile.mkdtemp()
    
    def test_enrich_entities_without_relationships(self):
        """Test enriching entities when no relationships are defined."""
        # Sample entities
        entities = [
            {
                "name": "Product",
                "fields": [
                    {"name": "id", "type": "Long", "annotations": ["@Id"]},
                    {"name": "name", "type": "String", "annotations": []}
                ]
            },
            {
                "name": "Category",
                "fields": [
                    {"name": "id", "type": "Long", "annotations": ["@Id"]},
                    {"name": "name", "type": "String", "annotations": []}
                ]
            }
        ]
        
        # Enrich entities
        enriched = self.mapper.enrich_entities(entities)
        
        # Should return original entities unchanged
        self.assertEqual(len(enriched), 2)
        self.assertEqual(len(enriched[0]["fields"]), 2)
        self.assertEqual(len(enriched[1]["fields"]), 2)
    
    def test_enrich_entities_with_relationships(self):
        """Test enriching entities with defined relationships."""
        # Sample entities
        entities = [
            {
                "name": "Product",
                "fields": [
                    {"name": "id", "type": "Long", "annotations": ["@Id"]},
                    {"name": "name", "type": "String", "annotations": []}
                ]
            },
            {
                "name": "Category",
                "fields": [
                    {"name": "id", "type": "Long", "annotations": ["@Id"]},
                    {"name": "name", "type": "String", "annotations": []}
                ]
            }
        ]
        
        # Set up relationships
        self.mapper.relationships = {
            "Product": [
                {
                    "target": "Category",
                    "type": "many-to-one",
                    "fieldName": "category"
                }
            ],
            "Category": [
                {
                    "target": "Product",
                    "type": "one-to-many",
                    "fieldName": "products"
                }
            ]
        }
        
        # Enrich entities
        enriched = self.mapper.enrich_entities(entities)
        
        # Verify Product entity has a category field
        product_entity = next(e for e in enriched if e["name"] == "Product")
        category_entity = next(e for e in enriched if e["name"] == "Category")
        
        self.assertEqual(len(product_entity["fields"]), 3)
        self.assertEqual(len(category_entity["fields"]), 3)
        
        # Check the relationship fields
        product_category_field = next(
            (f for f in product_entity["fields"] if f["name"] == "category"), None
        )
        self.assertIsNotNone(product_category_field)
        self.assertEqual(product_category_field["type"], "Category")
        self.assertTrue("@ManyToOne" in product_category_field["annotations"])
        
        category_products_field = next(
            (f for f in category_entity["fields"] if f["name"] == "productsList"), None
        )
        self.assertIsNotNone(category_products_field)
        self.assertEqual(category_products_field["type"], "List<Product>")
        self.assertTrue("@OneToMany" in category_products_field["annotations"][0])
    
    def test_generate_mapping_file(self):
        """Test generating a mapping file template."""
        # Sample entities
        entities = [
            {"name": "Product", "fields": []},
            {"name": "Category", "fields": []},
            {"name": "Order", "fields": []}
        ]
        
        # Output file path
        output_file = os.path.join(self.temp_dir, "mapping.json")
        
        # Generate mapping file
        self.mapper.generate_mapping_file(entities, output_file)
        
        # Verify file was created
        self.assertTrue(os.path.exists(output_file))
        
        # Load and verify content
        with open(output_file, "r") as f:
            mapping = json.load(f)
        
        # Check mapping structure
        self.assertEqual(len(mapping), 3)
        self.assertIn("Product", mapping)
        self.assertIn("Category", mapping)
        self.assertIn("Order", mapping)
        
        # Each entity should have relationships with all other entities
        self.assertEqual(len(mapping["Product"]), 2)  # Category, Order
        self.assertEqual(len(mapping["Category"]), 2)  # Product, Order
        self.assertEqual(len(mapping["Order"]), 2)  # Product, Category
    
    def test_analyze_entity_fields(self):
        """Test analyzing entity fields to detect relationships."""
        # Sample entities
        entities = [
            {
                "name": "Product",
                "fields": [
                    {"name": "id", "type": "Long", "annotations": ["@Id"]},
                    {"name": "name", "type": "String", "annotations": []},
                    {"name": "categoryId", "type": "Long", "annotations": []},
                    {"name": "tags", "type": "List<Tag>", "annotations": []}
                ]
            },
            {
                "name": "Category",
                "fields": [
                    {"name": "id", "type": "Long", "annotations": ["@Id"]},
                    {"name": "name", "type": "String", "annotations": []}
                ]
            },
            {
                "name": "Tag",
                "fields": [
                    {"name": "id", "type": "Long", "annotations": ["@Id"]},
                    {"name": "name", "type": "String", "annotations": []},
                    {"name": "product", "type": "Product", "annotations": []}
                ]
            }
        ]
        
        # Analyze entity fields
        detected = self.mapper.analyze_entity_fields(entities)
        
        # Verify detected relationships
        self.assertIn("Product", detected)
        self.assertIn("Tag", detected)
        
        # Check Product relationships
        product_rels = detected["Product"]
        self.assertEqual(len(product_rels), 2)  # categoryId, tags
        
        # Check Tag relationships
        tag_rels = detected["Tag"]
        self.assertEqual(len(tag_rels), 1)  # product
        self.assertEqual(tag_rels[0]["target"], "Product")
        self.assertEqual(tag_rels[0]["type"], "many-to-one")


if __name__ == "__main__":
    unittest.main()

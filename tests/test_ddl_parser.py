"""Tests for the DDL parser."""

import os
import unittest
import tempfile
from microgenesis.generators.schema.ddl_parser import DDLParser

class TestDDLParser(unittest.TestCase):
    """Test cases for the DDL parser."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = DDLParser()
        
        # Create a temporary DDL file
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".sql", delete=False)
        with open(self.temp_file.name, "w") as f:
            f.write("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                order_date DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            
            CREATE TABLE order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                product_name VARCHAR(100) NOT NULL,
                quantity INT NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            );
            """)
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.unlink(self.temp_file.name)
    
    def test_parse_ddl_file(self):
        """Test parsing a DDL file."""
        tables = self.parser.parse_ddl_file(self.temp_file.name)
        
        self.assertEqual(len(tables), 3)
        self.assertIn("users", [t["name"] for t in tables])
        self.assertIn("orders", [t["name"] for t in tables])
        self.assertIn("order_items", [t["name"] for t in tables])
        
        # Check table structures
        users_table = next(t for t in tables if t["name"] == "users")
        self.assertEqual(len(users_table["columns"]), 4)
        self.assertEqual(users_table["primaryKey"], ["id"])
        self.assertEqual(len(users_table["foreignKeys"]), 0)
        
        # Check relationships
        orders_table = next(t for t in tables if t["name"] == "orders")
        self.assertEqual(len(orders_table["foreignKeys"]), 1)
        self.assertEqual(orders_table["foreignKeys"][0]["referencedTable"], "users")
        
        # Verify relationships were identified
        self.assertTrue(any(r["type"] == "ManyToOne" for r in orders_table["relationships"]))
        self.assertTrue(any(r["type"] == "OneToMany" for r in users_table["relationships"]))
    
    def test_generate_java_entity(self):
        """Test generating a Java entity from table definition."""
        tables = self.parser.parse_ddl_file(self.temp_file.name)
        users_table = next(t for t in tables if t["name"] == "users")
        
        java_code = self.parser._generate_java_entity(users_table, "spring-boot")
        
        self.assertIn("@Entity", java_code)
        self.assertIn("@Table(name = \"users\")", java_code)
        self.assertIn("private Integer id;", java_code)
        self.assertIn("@Id", java_code)
        
    def test_generate_kotlin_entity(self):
        """Test generating a Kotlin entity from table definition."""
        tables = self.parser.parse_ddl_file(self.temp_file.name)
        users_table = next(t for t in tables if t["name"] == "users")
        
        kotlin_code = self.parser._generate_kotlin_entity(users_table, "spring-boot")
        
        self.assertIn("@Entity", kotlin_code)
        self.assertIn("@Table(name = \"users\")", kotlin_code)
        self.assertIn("@Id", kotlin_code)
        self.assertIn("val id: Int", kotlin_code)


if __name__ == "__main__":
    unittest.main()

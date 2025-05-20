"""DDL parser for generating entities from SQL schema."""

import re
from typing import Dict, List, Any, Tuple, Set, Optional
from microgenesis.logging import get_logger

logger = get_logger()

class DDLParser:
    """Parser for SQL DDL scripts to generate entity models."""
    
    def __init__(self):
        """Initialize the DDL parser."""
        self.logger = get_logger()
        
    def parse_ddl_file(self, ddl_file_path: str) -> List[Dict[str, Any]]:
        """Parse a DDL file and extract table definitions.
        
        Args:
            ddl_file_path: Path to the DDL file
            
        Returns:
            List[Dict[str, Any]]: List of table definitions
        """
        try:
            with open(ddl_file_path, 'r') as f:
                ddl_content = f.read()
            return self.parse_ddl(ddl_content)
        except Exception as e:
            self.logger.error(f"Error parsing DDL file {ddl_file_path}: {e}")
            return []
    
    def parse_ddl(self, ddl_content: str) -> List[Dict[str, Any]]:
        """Parse DDL content and extract table definitions.
        
        Args:
            ddl_content: SQL DDL content as string
            
        Returns:
            List[Dict[str, Any]]: List of table definitions
        """
        tables = []
        
        # Extract CREATE TABLE statements
        table_pattern = r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`\"]?(\w+)[`\"]?\s*\(([\s\S]*?)\)[\s\S]*?(?:;|$)"
        table_matches = re.finditer(table_pattern, ddl_content, re.IGNORECASE)
        
        # Process each table definition
        for table_match in table_matches:
            table_name = table_match.group(1)
            columns_content = table_match.group(2)
            
            # Extract columns and constraints
            columns, primary_keys, foreign_keys = self._parse_columns_and_constraints(columns_content)
            
            table = {
                'name': table_name,
                'className': self._to_camel_case(table_name),
                'columns': columns,
                'primaryKey': primary_keys,
                'foreignKeys': foreign_keys,
                'relationships': []
            }
            
            tables.append(table)
        
        # Process relationships after all tables are parsed
        self._process_relationships(tables)
        
        return tables
    
    def _parse_columns_and_constraints(self, columns_content: str) -> Tuple[List[Dict[str, Any]], List[str], List[Dict[str, Any]]]:
        """Parse columns and constraints from a table definition.
        
        Args:
            columns_content: Content inside the CREATE TABLE parentheses
            
        Returns:
            Tuple containing:
            - List of column definitions
            - List of primary key column names
            - List of foreign key definitions
        """
        columns = []
        primary_keys = []
        foreign_keys = []
        
        # Split by commas, but handle parentheses properly
        lines = self._split_preserving_parentheses(columns_content)
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Primary Key constraint
            if re.search(r'PRIMARY\s+KEY', line, re.IGNORECASE):
                pk_cols = re.search(r'\((.*?)\)', line)
                if pk_cols:
                    pk_cols = pk_cols.group(1)
                    for col in pk_cols.split(','):
                        col = col.strip().strip('`"')
                        primary_keys.append(col)
            
            # Foreign Key constraint
            elif re.search(r'FOREIGN\s+KEY', line, re.IGNORECASE):
                fk_col = re.search(r'FOREIGN\s+KEY\s*\(\s*[`"]?(\w+)[`"]?\s*\)', line, re.IGNORECASE)
                ref_table = re.search(r'REFERENCES\s+[`"]?(\w+)[`"]?', line, re.IGNORECASE)
                ref_col = re.search(r'REFERENCES\s+[`"]?\w+[`"]?\s*\(\s*[`"]?(\w+)[`"]?\s*\)', line, re.IGNORECASE)
                
                if fk_col and ref_table and ref_col:
                    foreign_key = {
                        'column': fk_col.group(1),
                        'referencedTable': ref_table.group(1),
                        'referencedColumn': ref_col.group(1)
                    }
                    foreign_keys.append(foreign_key)
            
            # Regular column definition
            elif not re.search(r'CONSTRAINT|INDEX|KEY', line, re.IGNORECASE):
                col_def = re.search(r'[`"]?(\w+)[`"]?\s+(\w+(?:\s*\(\s*\d+\s*(?:,\s*\d+\s*)?\))?)', line, re.IGNORECASE)
                if col_def:
                    col_name = col_def.group(1)
                    col_type = col_def.group(2)
                    
                    # Check for NOT NULL and DEFAULT
                    nullable = not bool(re.search(r'NOT\s+NULL', line, re.IGNORECASE))
                    default_match = re.search(r'DEFAULT\s+([^,]+)', line, re.IGNORECASE)
                    default_value = default_match.group(1).strip() if default_match else None
                    
                    columns.append({
                        'name': col_name,
                        'fieldName': self._to_camel_case(col_name, False),  # Start with lowercase for field names
                        'type': col_type.upper(),
                        'nullable': nullable,
                        'default': default_value
                    })
        
        return columns, primary_keys, foreign_keys
    
    def _process_relationships(self, tables: List[Dict[str, Any]]) -> None:
        """Process relationships between tables based on foreign keys.
        
        Args:
            tables: List of table definitions
        """
        # Create a mapping of table name to table definition for easy lookup
        table_map = {table['name']: table for table in tables}
        
        # Iterate through tables to identify relationships
        for table in tables:
            for fk in table['foreignKeys']:
                if fk['referencedTable'] in table_map:
                    referenced_table = table_map[fk['referencedTable']]
                    
                    # Add Many-to-One relationship from current table to referenced table
                    table['relationships'].append({
                        'type': 'ManyToOne',
                        'targetEntity': referenced_table['className'],
                        'fieldName': self._to_camel_case(fk['referencedTable'], False),
                        'joinColumn': fk['column']
                    })
                    
                    # Add One-to-Many relationship from referenced table to current table
                    referenced_table['relationships'].append({
                        'type': 'OneToMany',
                        'targetEntity': table['className'],
                        'fieldName': self._to_camel_case(table['name'] + 's', False),
                        'mappedBy': self._to_camel_case(fk['referencedTable'], False)
                    })
        
        # Look for Many-to-Many relationships (junction tables)
        for table in tables:
            if len(table['foreignKeys']) >= 2 and len(table['columns']) <= 3:  # Potential junction table
                self._process_junction_table(table, table_map)
    
    def _process_junction_table(self, junction_table: Dict[str, Any], table_map: Dict[str, Dict[str, Any]]) -> None:
        """Process a potential junction table for Many-to-Many relationships.
        
        Args:
            junction_table: Potential junction table definition
            table_map: Mapping of table names to table definitions
        """
        if len(junction_table['foreignKeys']) != 2:
            return  # Only consider tables with exactly 2 foreign keys as junction tables
        
        fk1 = junction_table['foreignKeys'][0]
        fk2 = junction_table['foreignKeys'][1]
        
        if fk1['referencedTable'] in table_map and fk2['referencedTable'] in table_map:
            table1 = table_map[fk1['referencedTable']]
            table2 = table_map[fk2['referencedTable']]
            
            # Add Many-to-Many relationship from table1 to table2
            table1['relationships'].append({
                'type': 'ManyToMany',
                'targetEntity': table2['className'],
                'fieldName': self._to_camel_case(table2['name'] + 's', False),
                'joinTable': {
                    'name': junction_table['name'],
                    'joinColumn': fk1['column'],
                    'inverseJoinColumn': fk2['column']
                }
            })
            
            # Add Many-to-Many relationship from table2 to table1
            table2['relationships'].append({
                'type': 'ManyToMany',
                'targetEntity': table1['className'],
                'fieldName': self._to_camel_case(table1['name'] + 's', False),
                'joinTable': {
                    'name': junction_table['name'],
                    'joinColumn': fk2['column'],
                    'inverseJoinColumn': fk1['column']
                }
            })
            
            # Mark this table as a junction table
            junction_table['isJunctionTable'] = True
    
    def _to_camel_case(self, snake_str: str, capitalize_first: bool = True) -> str:
        """Convert snake_case to CamelCase.
        
        Args:
            snake_str: String in snake_case
            capitalize_first: Whether to capitalize the first letter
            
        Returns:
            String in CamelCase
        """
        components = snake_str.split('_')
        if capitalize_first:
            return ''.join(x.title() for x in components)
        else:
            return components[0] + ''.join(x.title() for x in components[1:])
    
    def _split_preserving_parentheses(self, text: str) -> List[str]:
        """Split a string by commas while preserving content inside parentheses.
        
        Args:
            text: String to split
            
        Returns:
            List of strings
        """
        result = []
        current = ""
        paren_level = 0
        
        for char in text:
            if char == '(' and not paren_level:
                paren_level = 1
                current += char
            elif char == '(' and paren_level:
                paren_level += 1
                current += char
            elif char == ')' and paren_level > 1:
                paren_level -= 1
                current += char
            elif char == ')' and paren_level == 1:
                paren_level = 0
                current += char
            elif char == ',' and not paren_level:
                result.append(current)
                current = ""
            else:
                current += char
                
        if current:
            result.append(current)
            
        return result
    
    def _map_sql_to_java_type(self, sql_type: str) -> str:
        """Map SQL data type to Java type.
        
        Args:
            sql_type: SQL data type
            
        Returns:
            Corresponding Java type
        """
        sql_type = sql_type.lower()
        
        if re.search(r'int|tinyint|smallint|mediumint', sql_type):
            return 'Integer'
        elif re.search(r'bigint', sql_type):
            return 'Long'
        elif re.search(r'decimal|numeric|float', sql_type):
            return 'Double'
        elif re.search(r'double', sql_type):
            return 'Double'
        elif re.search(r'boolean|bit', sql_type):
            return 'Boolean'
        elif re.search(r'date', sql_type):
            return 'java.time.LocalDate'
        elif re.search(r'time', sql_type):
            return 'java.time.LocalTime'
        elif re.search(r'datetime|timestamp', sql_type):
            return 'java.time.LocalDateTime'
        elif re.search(r'blob|binary', sql_type):
            return 'byte[]'
        else:
            return 'String'  # Default for varchar, char, text, etc.
    
    def generate_entities(self, tables: List[Dict[str, Any]], language: str, framework: str) -> Dict[str, str]:
        """Generate entity code from table definitions.
        
        Args:
            tables: List of table definitions
            language: Target programming language ('java' or 'kotlin')
            framework: Target framework ('spring-boot' or 'micronaut')
            
        Returns:
            Dict[str, str]: Map of entity class names to generated code
        """
        entities = {}
        
        for table in tables:
            # Skip junction tables as they are represented through @ManyToMany in JPA
            if table.get('isJunctionTable', False):
                continue
                
            if language == 'java':
                code = self._generate_java_entity(table, framework)
            elif language == 'kotlin':
                code = self._generate_kotlin_entity(table, framework)
            else:
                self.logger.warning(f"Unsupported language: {language}")
                continue
                
            entities[table['className']] = code
            
        return entities
    
    def _generate_java_entity(self, table: Dict[str, Any], framework: str) -> str:
        """Generate Java entity code from table definition.
        
        Args:
            table: Table definition
            framework: Target framework
            
        Returns:
            str: Generated Java entity code
        """
        # This is a placeholder - implementation would depend on your specific templating approach
        # In a real implementation, you'd use a template engine like Jinja2
        # Here we're just showing the structure
        
        imports = [
            "import javax.persistence.*;"
        ]
        
        for rel in table['relationships']:
            imports.append("import java.util.List;")
            break
            
        class_definition = f"@Entity\n@Table(name = \"{table['name']}\")\npublic class {table['className']} {{"
        
        fields = []
        for col in table['columns']:
            java_type = self._map_sql_to_java_type(col['type'])
            nullable_annotation = "" if col['nullable'] else "@Column(nullable = false)"
            
            if col['name'] in table['primaryKey']:
                field = f"    @Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)\n    private {java_type} {col['fieldName']};"
            else:
                field = f"    {nullable_annotation}\n    private {java_type} {col['fieldName']};"
                
            fields.append(field)
            
        # Add relationship fields
        for rel in table['relationships']:
            if rel['type'] == 'ManyToOne':
                field = f"    @ManyToOne\n    @JoinColumn(name = \"{rel['joinColumn']}\")\n    private {rel['targetEntity']} {rel['fieldName']};"
                fields.append(field)
            elif rel['type'] == 'OneToMany':
                field = f"    @OneToMany(mappedBy = \"{rel['mappedBy']}\")\n    private List<{rel['targetEntity']}> {rel['fieldName']};"
                fields.append(field)
            elif rel['type'] == 'ManyToMany':
                join_table = rel['joinTable']
                field = f'    @ManyToMany\n    @JoinTable(name = "{join_table["name"]}", \n        joinColumns = @JoinColumn(name = "{join_table["joinColumn"]}"), \n        inverseJoinColumns = @JoinColumn(name = "{join_table["inverseJoinColumn"]}") \n    )\n    private List<{rel["targetEntity"]}> {rel["fieldName"]};'
                fields.append(field)
                
        # Generate getters and setters (abbreviated for this example)
        methods = []
        
        return "\n".join(imports) + "\n\n" + class_definition + "\n\n" + "\n\n".join(fields) + "\n\n" + "\n\n".join(methods) + "\n}"
    
    def _generate_kotlin_entity(self, table: Dict[str, Any], framework: str) -> str:
        """Generate Kotlin entity code from table definition.
        
        Args:
            table: Table definition
            framework: Target framework
            
        Returns:
            str: Generated Kotlin entity code
        """
        # Similar to Java generation but with Kotlin syntax
        imports = [
            "import javax.persistence.*"
        ]
        
        for rel in table['relationships']:
            if rel['type'] in ['OneToMany', 'ManyToMany']:
                imports.append("import java.util.List")
                break
            
        class_start = "@Entity\n@Table(name = \"${table['name']}\")\ndata class ${table['className']}("
        
        fields = []
        for col in table['columns']:
            kotlin_type = self._map_sql_to_kotlin_type(col['type'])
            nullable_suffix = "?" if col['nullable'] else ""
            
            if col['name'] in table['primaryKey']:
                field = f"    @Id\n    @GeneratedValue(strategy = GenerationType.IDENTITY)\n    val {col['fieldName']}: {kotlin_type}{nullable_suffix},"
            else:
                field = f"    @Column(nullable = {str(col['nullable']).lower()})\n    val {col['fieldName']}: {kotlin_type}{nullable_suffix},"
                
            fields.append(field)
            
        # Simplified for this example
        return "\n".join(imports) + "\n\n" + class_start + "\n" + "\n".join(fields) + "\n)"
    
    def _map_sql_to_kotlin_type(self, sql_type: str) -> str:
        """Map SQL data type to Kotlin type.
        
        Args:
            sql_type: SQL data type
            
        Returns:
            Corresponding Kotlin type
        """
        sql_type = sql_type.lower()
        
        if re.search(r'int|tinyint|smallint|mediumint', sql_type):
            return 'Int'
        elif re.search(r'bigint', sql_type):
            return 'Long'
        elif re.search(r'decimal|numeric|float', sql_type):
            return 'Double'
        elif re.search(r'double', sql_type):
            return 'Double'
        elif re.search(r'boolean|bit', sql_type):
            return 'Boolean'
        elif re.search(r'date', sql_type):
            return 'java.time.LocalDate'
        elif re.search(r'time', sql_type):
            return 'java.time.LocalTime'
        elif re.search(r'datetime|timestamp', sql_type):
            return 'java.time.LocalDateTime'
        elif re.search(r'blob|binary', sql_type):
            return 'ByteArray'
        else:
            return 'String'  # Default for varchar, char, text, etc.

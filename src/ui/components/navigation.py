"""Navigation and UI rendering functions for MicroGenesis."""

import streamlit as st
import pandas as pd
from src.ui.utils.helpers import update_selection
from src.ui.styles.css import apply_custom_css
from src.ui.utils.core_integration import parse_ddl_file


def render_step_1_ui(languages, frameworks, build_tools, pipelines, databases, features, service_types):
    """Render the first step of the UI - Project Configuration.
    
    Args:
        languages: List of language options
        frameworks: List of framework options
        build_tools: List of build tool options
        pipelines: List of CI/CD pipeline options
        databases: List of database options
        features: List of additional feature options
        service_types: List of service architecture types
    """
    st.header("Project Configuration")
    
    # Project basics
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.projectName = st.text_input(
                "Project Name", 
                value=st.session_state.projectName,
                help="Name of your microservice project"
            )
        with col2:
            st.session_state.basePackageName = st.text_input(
                "Base Package", 
                value=st.session_state.basePackageName,
                help="Base package name for your Java/Kotlin code"
            )
    
    # Create tabs for organization
    tabs = st.tabs(["Language & Framework", "Build & Database", "Service Architecture", "Features"])
    
    # Tab 1: Language & Framework
    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            # Language selection
            lang_names = [l["name"] for l in languages]
            selected_lang_idx = 0
            if st.session_state.selections['language'] and st.session_state.selections['language']['name'] in lang_names:
                selected_lang_idx = lang_names.index(st.session_state.selections['language']['name'])
                
            selected_lang_name = st.selectbox(
                "Select Language", 
                lang_names, 
                index=selected_lang_idx,
                help="Programming language for your project"
            )
            selected_lang = next(l for l in languages if l["name"] == selected_lang_name)
            update_selection('language', selected_lang)
            
            # Language version selection
            lang_version_names = [v["name"] for v in selected_lang["versions"]]
            recommended_idx = next(i for i, v in enumerate(selected_lang["versions"]) if v["recommended"])
            
            selected_lang_ver_idx = recommended_idx
            if st.session_state.selections['languageVersion'] and st.session_state.selections['languageVersion']['name'] in lang_version_names:
                selected_lang_ver_idx = lang_version_names.index(st.session_state.selections['languageVersion']['name'])
                
            selected_lang_ver_name = st.radio(
                "Language Version",
                lang_version_names,
                index=selected_lang_ver_idx
            )
            selected_lang_version = next(v for v in selected_lang["versions"] if v["name"] == selected_lang_ver_name)
            update_selection('languageVersion', selected_lang_version)
            
        with col2:
            # Framework selection
            framework_names = [f["name"] for f in frameworks]
            selected_framework_idx = 0
            if st.session_state.selections['framework'] and st.session_state.selections['framework']['name'] in framework_names:
                selected_framework_idx = framework_names.index(st.session_state.selections['framework']['name'])
                
            selected_framework_name = st.selectbox(
                "Framework", 
                framework_names, 
                index=selected_framework_idx,
                help="Web framework for your microservice"
            )
            selected_framework = next(f for f in frameworks if f["name"] == selected_framework_name)
            update_selection('framework', selected_framework)
            
            # Framework version selection
            framework_version_names = [v["name"] for v in selected_framework["versions"]]
            recommended_idx = next(i for i, v in enumerate(selected_framework["versions"]) if v["recommended"])
            
            selected_framework_ver_idx = recommended_idx
            if st.session_state.selections['frameworkVersion'] and st.session_state.selections['frameworkVersion']['name'] in framework_version_names:
                selected_framework_ver_idx = framework_version_names.index(st.session_state.selections['frameworkVersion']['name'])
                
            selected_framework_ver_name = st.radio(
                "Framework Version",
                framework_version_names,
                index=selected_framework_ver_idx
            )
            selected_framework_version = next(v for v in selected_framework["versions"] if v["name"] == selected_framework_ver_name)
            update_selection('frameworkVersion', selected_framework_version)
    
    # Tab 2: Build & Database
    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            # Build tool selection
            build_tool_names = [b["name"] for b in build_tools]
            selected_build_tool_idx = 0
            if st.session_state.selections['buildTool'] and st.session_state.selections['buildTool']['name'] in build_tool_names:
                selected_build_tool_idx = build_tool_names.index(st.session_state.selections['buildTool']['name'])
                
            selected_build_tool_name = st.selectbox(
                "Build Tool", 
                build_tool_names, 
                index=selected_build_tool_idx,
                help="Build system for your project"
            )
            selected_build_tool = next(b for b in build_tools if b["name"] == selected_build_tool_name)
            update_selection('buildTool', selected_build_tool)
            
            # Gradle DSL selection if Gradle is chosen
            if selected_build_tool["id"] == "gradle" and "dsl_options" in selected_build_tool:
                dsl_options = [d["name"] for d in selected_build_tool["dsl_options"]]
                selected_dsl_idx = 0
                if st.session_state.selections['gradleDsl'] and st.session_state.selections['gradleDsl']['name'] in dsl_options:
                    selected_dsl_idx = dsl_options.index(st.session_state.selections['gradleDsl']['name'])
                    
                selected_dsl_name = st.radio(
                    "Gradle DSL", 
                    dsl_options,
                    index=selected_dsl_idx,
                    help="DSL to use for Gradle build scripts"
                )
                selected_dsl = next(d for d in selected_build_tool["dsl_options"] if d["name"] == selected_dsl_name)
                update_selection('gradleDsl', selected_dsl)
            
            # Pipeline selection
            pipeline_names = [p["name"] for p in pipelines]
            selected_pipeline_idx = 0
            if st.session_state.selections['pipeline'] and st.session_state.selections['pipeline']['name'] in pipeline_names:
                selected_pipeline_idx = pipeline_names.index(st.session_state.selections['pipeline']['name'])
                
            selected_pipeline_name = st.selectbox(
                "CI/CD Pipeline", 
                pipeline_names, 
                index=selected_pipeline_idx,
                help="Continuous integration and deployment pipeline"
            )
            selected_pipeline = next(p for p in pipelines if p["name"] == selected_pipeline_name)
            update_selection('pipeline', selected_pipeline)
            
        with col2:
            # Database selection
            db_names = [d["name"] for d in databases]
            selected_db_idx = 0
            if st.session_state.selections['database'] and st.session_state.selections['database']['name'] in db_names:
                selected_db_idx = db_names.index(st.session_state.selections['database']['name'])
                
            selected_db_name = st.selectbox(
                "Database", 
                db_names, 
                index=selected_db_idx,
                help="Database for your microservice"
            )
            selected_db = next(d for d in databases if d["name"] == selected_db_name)
            update_selection('database', selected_db)
            
            # Database connection fields if a database is selected
            if selected_db["id"] != "none":
                st.text_input(
                    f"{selected_db['name']} URL", 
                    value="jdbc:postgresql://localhost:5432/dbname" if selected_db["id"] == "postgresql" 
                          else "jdbc:mysql://localhost:3306/dbname" if selected_db["id"] == "mysql"
                          else "jdbc:h2:mem:testdb" if selected_db["id"] == "h2"
                          else "mongodb://localhost:27017/dbname",
                    help="Database connection URL"
                )
            
    # Tab 3: Service Architecture
    with tabs[2]:
        # Service type selection
        st.write("Select the architectural style for your microservice:")
        
        service_type_names = [s["name"] for s in service_types]
        selected_service_type_idx = 0
        if st.session_state.selections['serviceType'] and st.session_state.selections['serviceType']['name'] in service_type_names:
            selected_service_type_idx = service_type_names.index(st.session_state.selections['serviceType']['name'])
            
        selected_service_type_name = st.selectbox(
            "Architectural Style", 
            service_type_names, 
            index=selected_service_type_idx,
            help="Architectural approach for your microservice"
        )
        selected_service_type = next(s for s in service_types if s["name"] == selected_service_type_name)
        update_selection('serviceType', selected_service_type)
        
        # Show description of selected style
        st.info(selected_service_type["description"])
        
        # Show package structure preview based on selected style
        st.subheader("Package Structure Preview")
        package_base = st.session_state.basePackageName.replace(".", "/")
        
        if selected_service_type["id"] == "domain-driven":
            st.code(f"""
src/main/java/{package_base}/
├── domain/
│   ├── model/
│   ├── repository/
│   └── service/
├── application/
│   ├── dto/
│   ├── controller/
│   └── exception/
├── infrastructure/
│   ├── config/
│   ├── persistence/
│   └── security/
└── {st.session_state.projectName}Application.java
            """)
        elif selected_service_type["id"] == "entity-driven":
            st.code(f"""
src/main/java/{package_base}/
├── entity/
├── repository/
├── service/
├── controller/
├── dto/
├── mapper/
├── exception/
├── config/
└── {st.session_state.projectName}Application.java
            """)
        else:
            st.code(f"""
src/main/java/{package_base}/
├── controller/
├── service/
├── repository/
├── model/
├── config/
└── {st.session_state.projectName}Application.java
            """)
    
    # Tab 4: Features
    with tabs[3]:
        st.write("Select additional features for your microservice:")
        
        # Display features as checkboxes
        selected_features = []
        for feature in features:
            if st.checkbox(
                feature["name"], 
                value=any(f["id"] == feature["id"] for f in st.session_state.selections["features"]),
                help=feature["description"]
            ):
                selected_features.append(feature)
        
        # Update selected features in session state
        update_selection('features', selected_features)
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Next: Entity Configuration →", type="primary", use_container_width=True):
            st.session_state.step = 2
            st.rerun()


def render_step_2_ui():
    """Render the second step of the UI - Entity Configuration."""
    st.header("Entity Configuration")
    
    # Create tabs for different entity creation methods
    tabs = st.tabs(["Import from DDL", "Manually Design Entities", "Entity List", "Relationship Mapper"])
    
    # Tab 1: Import from DDL
    with tabs[0]:
        st.write("Upload a SQL DDL file to automatically generate entities.")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            ddl_file = st.file_uploader("Upload DDL File", type=["sql"], key="ddl_uploader")
            
        with col2:
            preview_btn = st.button("Preview Entities", use_container_width=True, disabled=not ddl_file)
        
        # Handle the DDL file
        if ddl_file:
            st.session_state.ddlFile = ddl_file
            ddl_content = ddl_file.getvalue().decode("utf-8")
            st.session_state.selections['ddl'] = ddl_content
            
            # Preview area for DDL content
            st.text_area("DDL Content Preview", ddl_content[:1000] + ("..." if len(ddl_content) > 1000 else ""), height=150)
            
            if preview_btn:
                with st.spinner("Parsing DDL and generating entities..."):
                    try:
                        parsed_entities = parse_ddl_file(ddl_content)
                        
                        if parsed_entities:
                            # Show preview of parsed entities in a table
                            entity_display_data = []
                            for entity in parsed_entities:
                                entity_display_data.append({
                                    "Entity Name": entity["name"],
                                    "Table Name": entity.get("tableName", entity["name"].lower()),
                                    "Fields": len(entity["fields"]),
                                    "Has Primary Key": any(f.get("primaryKey") for f in entity["fields"])
                                })
                            
                            st.subheader(f"Found {len(parsed_entities)} Entities")
                            st.dataframe(pd.DataFrame(entity_display_data), use_container_width=True)
                            
                            # Button to import entities
                            if st.button("Import These Entities", type="primary"):
                                # Add the entities to the session state
                                existing_entity_names = {e["name"] for e in st.session_state.entities}
                                
                                for entity in parsed_entities:
                                    if entity["name"] not in existing_entity_names:
                                        st.session_state.entities.append(entity)
                                        existing_entity_names.add(entity["name"])
                                
                                st.success(f"Successfully imported {len(parsed_entities)} entities from DDL")
                                st.rerun()
                        else:
                            st.warning("No entities found in the DDL file")
                    except Exception as e:
                        st.error(f"Error parsing DDL: {str(e)}")
    
    # Tab 2: Manual Entity Design
    with tabs[1]:
        st.subheader("Create New Entity")
        
        with st.form("entity_form"):
            entity_name = st.text_input("Entity Name", key="new_entity_name")
            entity_table = st.text_input("Table Name", key="new_entity_table", 
                                       help="Leave empty to use the entity name in lowercase")
            
            # Field management
            st.subheader("Fields")
            
            # Initialize temp_fields for the form if not exists
            if "temp_fields" not in st.session_state:
                st.session_state.temp_fields = []
            
            # Display existing fields if any
            if st.session_state.temp_fields:
                field_df = pd.DataFrame(st.session_state.temp_fields)
                st.dataframe(field_df, use_container_width=True)
            
            # Add new field
            st.subheader("Add Field")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                field_name = st.text_input("Field Name", key="new_field_name")
            
            with col2:
                field_type = st.selectbox(
                    "Field Type",
                    options=["String", "Integer", "Long", "Double", "Boolean", "Date", "DateTime", "Enum"],
                    key="new_field_type"
                )
            
            with col3:
                required = st.checkbox("Required", key="new_field_required")
            
            col4, col5 = st.columns(2)
            
            with col4:
                primary_key = st.checkbox("Primary Key", key="new_field_pk")
            
            with col5:
                unique = st.checkbox("Unique", key="new_field_unique")
            
            # Add field button
            add_field = st.form_submit_button("Add Field")
            if add_field and field_name:
                st.session_state.temp_fields.append({
                    "name": field_name,
                    "type": field_type,
                    "required": required,
                    "primaryKey": primary_key,
                    "unique": unique
                })
                
                # Reset field form
                st.session_state.new_field_name = ""
                st.session_state.new_field_required = False
                st.session_state.new_field_pk = False
                st.session_state.new_field_unique = False
                st.rerun()
            
            # Create entity button
            submit_entity = st.form_submit_button("Create Entity")
            
            if submit_entity and entity_name and st.session_state.temp_fields:
                # Create the entity
                new_entity = {
                    "name": entity_name,
                    "tableName": entity_table if entity_table else entity_name.lower(),
                    "fields": st.session_state.temp_fields.copy()
                }
                
                # Add to entities list
                st.session_state.entities.append(new_entity)
                
                # Reset the form
                st.session_state.new_entity_name = ""
                st.session_state.new_entity_table = ""
                st.session_state.temp_fields = []
                st.rerun()
    
    # Tab 3: Entity List
    with tabs[2]:
        st.subheader("Configured Entities")
        
        if not st.session_state.entities:
            st.info("No entities created yet. Use the DDL Import or Entity Creator to add entities.")
        else:
            for i, entity in enumerate(st.session_state.entities):
                with st.expander(f"{entity['name']} ({entity['tableName']})"):
                    if entity["fields"]:
                        field_data = [{
                            "Field": f['name'],
                            "Type": f['type'],
                            "Required": "✓" if f.get('required') else "",
                            "Primary Key": "✓" if f.get('primaryKey') else "",
                            "Unique": "✓" if f.get('unique') else ""
                        } for f in entity["fields"]]
                        st.dataframe(pd.DataFrame(field_data), hide_index=True, use_container_width=True)
                        
                        col1, col2 = st.columns([4, 1])
                        with col2:
                            if st.button("Delete Entity", key=f"del_entity_{i}"):
                                st.session_state.entities.pop(i)
                                st.rerun()
                    else:
                        st.write("No fields defined for this entity.")
    
    # Tab 4: Relationship Mapper
    with tabs[3]:
        st.subheader("Entity Relationship Mapper")
        
        if len(st.session_state.entities) < 2:
            st.info("You need at least 2 entities to define relationships. Create more entities first.")
        else:
            st.subheader("Create New Relationship")
            
            with st.form("relationship_form"):
                col1, col2, col3 = st.columns(3)
                
                entity_names = [entity["name"] for entity in st.session_state.entities]
                
                with col1:
                    source_entity = st.selectbox(
                        "Source Entity",
                        options=entity_names,
                        key="rel_source"
                    )
                
                with col2:
                    relationship_type = st.selectbox(
                        "Relationship Type",
                        options=["One-to-One", "One-to-Many", "Many-to-One", "Many-to-Many"],
                        key="rel_type"
                    )
                
                with col3:
                    target_entity = st.selectbox(
                        "Target Entity",
                        options=entity_names,
                        key="rel_target"
                    )
                
                col4, col5 = st.columns(2)
                
                with col4:
                    bidirectional = st.checkbox("Bidirectional", key="rel_bidirectional")
                
                with col5:
                    fetch_type = st.selectbox(
                        "Fetch Type",
                        options=["EAGER", "LAZY"],
                        key="rel_fetch"
                    )
                
                submit_rel = st.form_submit_button("Create Relationship")
                
                if submit_rel and source_entity and target_entity and source_entity != target_entity:
                    # Create the relationship
                    relationship = {
                        "sourceEntity": source_entity,
                        "targetEntity": target_entity,
                        "type": relationship_type,
                        "bidirectional": bidirectional,
                        "fetchType": fetch_type
                    }
                    
                    # Add to relationships list
                    st.session_state.relationships.append(relationship)
                    st.success(f"Relationship created: {source_entity} {relationship_type} {target_entity}")
                    st.rerun()
            
            # Display existing relationships
            if st.session_state.relationships:
                st.subheader("Defined Relationships")
                relationship_data = [{
                    "Source Entity": r['sourceEntity'],
                    "Relationship": r['type'],
                    "Target Entity": r['targetEntity'],
                    "Bidirectional": "✓" if r.get('bidirectional') else "",
                    "Fetch Type": r.get('fetchType', 'LAZY'),
                } for r in st.session_state.relationships]
                st.dataframe(pd.DataFrame(relationship_data), hide_index=True, use_container_width=True)
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back to Project Configuration", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    with col3:
        if st.button("Next: API Configuration →", type="primary", use_container_width=True):
            st.session_state.step = 3
            st.rerun()


def render_step_3_ui():
    """Render the third step of the UI - API Configuration."""
    st.header("API Configuration")
    
    with st.container():
        st.write("Upload a Swagger/OpenAPI specification file to generate API endpoints.")
        
        swagger_file = st.file_uploader(
            "Upload Swagger / OpenAPI file (JSON or YAML)",
            type=['json', 'yaml', 'yml'],
            key="swagger_uploader"
        )
        
        if swagger_file:
            swagger_content = swagger_file.read().decode("utf-8")
            st.session_state.selections['swagger'] = swagger_content
            st.session_state.swaggerFile = swagger_file
            
            st.success(f"Successfully uploaded {swagger_file.name}")
            
            # Preview the swagger content
            st.subheader("Swagger Preview")
            st.text_area("Content Preview", swagger_content[:1000] + ("..." if len(swagger_content) > 1000 else ""), height=200)
            
            # Alternatively, you can skip this step
            st.info("Swagger file is optional. You can generate your project without it.")
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back to Entity Configuration", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    with col3:
        if st.button("Next: Generate Project →", type="primary", use_container_width=True):
            st.session_state.step = 4
            st.rerun()


def render_step_4_ui(generate_zip_fn):
    """Render the fourth step of the UI - Project Generation.
    
    Args:
        generate_zip_fn: Function to generate the project zip file
    """
    apply_custom_css()
    
    st.header("Project Generation")
    
    # Construct HTML content for project summary
    summary_html = f"""
    <div class="summary-card">
        <h3>📦 Project Summary</h3>
        <div class="summary-row"><div class="summary-label">Project Name:</div><div class="summary-value">{st.session_state.projectName}</div></div>
        <div class="summary-row"><div class="summary-label">Base Package:</div><div class="summary-value">{st.session_state.basePackageName}</div></div>
        <div class="summary-row"><div class="summary-label">Language:</div><div class="summary-value">{st.session_state.selections['language']['name'] if st.session_state.selections['language'] else 'Not selected'}</div></div>
        <div class="summary-row"><div class="summary-label">Language Version:</div><div class="summary-value">{st.session_state.selections['languageVersion']['name'] if st.session_state.selections['languageVersion'] else 'Not selected'}</div></div>
        <div class="summary-row"><div class="summary-label">Framework:</div><div class="summary-value">{st.session_state.selections['framework']['name'] if st.session_state.selections['framework'] else 'Not selected'}</div></div>
        <div class="summary-row"><div class="summary-label">Framework Version:</div><div class="summary-value">{st.session_state.selections['frameworkVersion']['name'] if st.session_state.selections['frameworkVersion'] else 'Not selected'}</div></div>
        <div class="summary-row"><div class="summary-label">Build Tool:</div><div class="summary-value">{st.session_state.selections['buildTool']['name'] if st.session_state.selections['buildTool'] else 'Not selected'}</div></div>
        <div class="summary-row"><div class="summary-label">Service Architecture:</div><div class="summary-value">{st.session_state.selections['serviceType']['name'] if st.session_state.selections['serviceType'] else 'Not selected'}</div></div>
        <div class="summary-row"><div class="summary-label">Database:</div><div class="summary-value">{st.session_state.selections['database']['name'] if st.session_state.selections['database'] else 'Not selected'}</div></div>
        <div class="summary-row"><div class="summary-label">Pipeline:</div><div class="summary-value">{st.session_state.selections['pipeline']['name'] if st.session_state.selections['pipeline'] else 'Not selected'}</div></div>
        <div class="summary-row"><div class="summary-label">Features:</div><div class="summary-value">{', '.join([f['name'] for f in st.session_state.selections['features']]) or 'None'}</div></div>
        <div class="summary-row"><div class="summary-label">Entities:</div><div class="summary-value">{len(st.session_state.entities)} entities defined</div></div>
        <div class="summary-row"><div class="summary-label">Relationships:</div><div class="summary-value">{len(st.session_state.relationships)} relationships defined</div></div>
        <div class="summary-row"><div class="summary-label">Swagger File:</div><div class="summary-value">{st.session_state.swaggerFile.name if st.session_state.swaggerFile else 'Not uploaded'}</div></div>
        <div class="summary-row"><div class="summary-label">DDL File:</div><div class="summary-value">{st.session_state.ddlFile.name if st.session_state.ddlFile else 'Not uploaded'}</div></div>
    </div>
    """
    
    # Display project summary
    st.markdown(summary_html, unsafe_allow_html=True)
    
    # Generation actions
    st.subheader("Generate Project")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        output_dir = st.text_input(
            "Output Directory", 
            value="./output",
            help="Directory where the generated code will be placed"
        )
        
    with col2:
        # Generate button
        if st.button("Generate Project", type="primary", use_container_width=True):
            with st.spinner("Generating project..."):
                # Prepare config for generation
                from src.ui.utils.core_integration import prepare_config_from_ui, generate_project_from_ui
                
                # Set output directory
                st.session_state.output_dir = output_dir
                
                # Generate the project
                config = prepare_config_from_ui(st.session_state)
                project_path = generate_project_from_ui(config)
                
                if project_path and os.path.exists(project_path):
                    st.session_state.generated_path = project_path
                    st.session_state.show_download = True
                      # Save to project history
                    from src.ui.state.session_state import save_project_to_history
                    save_project_to_history()
                    
                    # Success message with project path
                    st.success(f"Project generated successfully at: {project_path}")
                    
                    # Show file structure
                    show_file_structure(project_path)
                else:
                    st.error("Failed to generate project. See logs for details.")
    
    # Download zip option
    if st.session_state.show_download and hasattr(st.session_state, 'generated_path'):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.download_button(
                label="Download Project as ZIP",
                data=generate_zip_fn(),
                file_name=f"{st.session_state.projectName}.zip",
                mime="application/zip",
            )
            
        with col2:
            # Open folder button
            if st.button("Open Project Folder"):
                import subprocess
                import os
                
                if os.path.exists(st.session_state.generated_path):
                    if os.name == 'nt':  # Windows
                        subprocess.Popen(f'explorer "{st.session_state.generated_path}"')
                    elif os.name == 'posix':  # macOS/Linux
                        subprocess.Popen(['open', st.session_state.generated_path])
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back to API Configuration", use_container_width=True):
            st.session_state.step = 3
            st.rerun()
    with col3:
        if st.button("Start Over", use_container_width=True):
            # Reset session state
            for key in list(st.session_state.keys()):
                if key != 'project_history':  # Preserve project history
                    del st.session_state[key]
            st.rerun()


def show_file_structure(project_path):
    """Display the file structure of the generated project.
    
    Args:
        project_path: Path to the generated project
    """
    import os
    
    st.subheader("Generated Project Structure")
    
    file_structure = []
    for root, dirs, files in os.walk(project_path):
        level = root.replace(project_path, '').count(os.sep)
        indent = ' ' * 4 * level
        folder = os.path.basename(root)
        file_structure.append(f"{indent}{folder}/")
        
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            file_structure.append(f"{sub_indent}{f}")
    
    # Limit to first 100 entries to prevent UI slowdown
    st.text("\n".join(file_structure[:100]))
    if len(file_structure) > 100:
        st.info(f"Showing first 100 of {len(file_structure)} files. The complete structure is available in the project directory.")

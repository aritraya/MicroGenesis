-- filepath: tests/resource/function_oriented_schema.sql
-- Function-Oriented Design Database Schema for Content Management System
-- Focused on action-based tables with minimal coupling between entities

-- Core Content Storage
CREATE TABLE content_items (
    content_id UUID PRIMARY KEY,
    content_type VARCHAR(20) NOT NULL CHECK (content_type IN ('ARTICLE', 'BLOG', 'PAGE', 'PRODUCT', 'NEWS')),
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('DRAFT', 'PUBLISHED', 'ARCHIVED', 'SCHEDULED')),
    locale VARCHAR(10) NOT NULL DEFAULT 'en-US',
    content_data JSONB NOT NULL, -- Stores the actual content structure
    metadata JSONB, -- For SEO and other metadata
    version VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) NOT NULL,
    updated_by VARCHAR(100) NOT NULL
);

CREATE UNIQUE INDEX idx_content_slug ON content_items(slug, locale) WHERE status = 'PUBLISHED';
CREATE INDEX idx_content_type_status ON content_items(content_type, status);
CREATE INDEX idx_content_created_at ON content_items(created_at);

-- Content Version History - Immutable log of content changes
CREATE TABLE content_versions (
    version_id UUID PRIMARY KEY,
    content_id UUID NOT NULL,
    version_number VARCHAR(50) NOT NULL,
    content_data JSONB NOT NULL,
    metadata JSONB,
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) NOT NULL,
    CONSTRAINT fk_content_versions FOREIGN KEY (content_id) REFERENCES content_items(content_id)
);

CREATE INDEX idx_content_versions_content_id ON content_versions(content_id);
CREATE INDEX idx_content_versions_created_at ON content_versions(created_at);

-- Media Storage
CREATE TABLE media_items (
    media_id UUID PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    size_bytes BIGINT NOT NULL,
    width INT,
    height INT,
    duration DECIMAL(10, 2),
    storage_path VARCHAR(500) NOT NULL,
    public_url VARCHAR(500) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) NOT NULL
);

CREATE INDEX idx_media_mime_type ON media_items(mime_type);
CREATE INDEX idx_media_created_at ON media_items(created_at);

-- Media Transformations
CREATE TABLE media_variants (
    variant_id UUID PRIMARY KEY,
    media_id UUID NOT NULL,
    variant_name VARCHAR(100) NOT NULL,
    width INT,
    height INT,
    format VARCHAR(20) NOT NULL,
    size_bytes BIGINT NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    public_url VARCHAR(500) NOT NULL,
    transformation_params JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_media_variants FOREIGN KEY (media_id) REFERENCES media_items(media_id)
);

CREATE INDEX idx_media_variants_media_id ON media_variants(media_id);

-- Function-oriented tables for common operations

-- Publishing Operations
CREATE TABLE publishing_operations (
    operation_id UUID PRIMARY KEY,
    content_id UUID NOT NULL,
    operation_type VARCHAR(20) NOT NULL CHECK (operation_type IN ('PUBLISH', 'UNPUBLISH', 'SCHEDULE')),
    scheduled_time TIMESTAMP,
    execution_time TIMESTAMP,
    channels JSONB NOT NULL, -- Array of channel identifiers
    status VARCHAR(20) NOT NULL CHECK (status IN ('PENDING', 'COMPLETED', 'FAILED', 'CANCELED')),
    error_message TEXT,
    expiration_date TIMESTAMP,
    notify_subscribers BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) NOT NULL,
    CONSTRAINT fk_publishing_content FOREIGN KEY (content_id) REFERENCES content_items(content_id)
);

CREATE INDEX idx_publishing_content_id ON publishing_operations(content_id);
CREATE INDEX idx_publishing_scheduled_time ON publishing_operations(scheduled_time) WHERE operation_type = 'SCHEDULE';
CREATE INDEX idx_publishing_status ON publishing_operations(status) WHERE status = 'PENDING';

-- Content Tagging - Function-oriented approach with action timestamps
CREATE TABLE content_tag_operations (
    operation_id UUID PRIMARY KEY,
    content_id UUID NOT NULL,
    tag_name VARCHAR(100) NOT NULL,
    operation_type VARCHAR(10) NOT NULL CHECK (operation_type IN ('ADD', 'REMOVE')),
    performed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    performed_by VARCHAR(100) NOT NULL,
    CONSTRAINT fk_content_tag_content FOREIGN KEY (content_id) REFERENCES content_items(content_id)
);

CREATE INDEX idx_content_tag_content_id ON content_tag_operations(content_id);
CREATE INDEX idx_content_tag_name ON content_tag_operations(tag_name);

-- Content Categorization - Function-oriented approach with action timestamps
CREATE TABLE content_category_operations (
    operation_id UUID PRIMARY KEY,
    content_id UUID NOT NULL,
    category_path VARCHAR(255) NOT NULL,
    operation_type VARCHAR(10) NOT NULL CHECK (operation_type IN ('ADD', 'REMOVE')),
    performed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    performed_by VARCHAR(100) NOT NULL,
    CONSTRAINT fk_content_category_content FOREIGN KEY (content_id) REFERENCES content_items(content_id)
);

CREATE INDEX idx_content_category_content_id ON content_category_operations(content_id);
CREATE INDEX idx_content_category_path ON content_category_operations(category_path);

-- Authentication Operations
CREATE TABLE auth_tokens (
    token_id UUID PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    token_type VARCHAR(20) NOT NULL,
    token_value VARCHAR(1000) NOT NULL,
    client_id VARCHAR(100) NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    permissions JSONB,
    issued_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    revoked BOOLEAN NOT NULL DEFAULT FALSE,
    revoked_at TIMESTAMP,
    revoked_reason VARCHAR(255)
);

CREATE INDEX idx_auth_tokens_user_id ON auth_tokens(user_id);
CREATE INDEX idx_auth_tokens_expires_at ON auth_tokens(expires_at) WHERE revoked = FALSE;
CREATE INDEX idx_auth_tokens_token_value ON auth_tokens(token_value) WHERE revoked = FALSE;

-- URL Shortening Operations
CREATE TABLE shortened_urls (
    url_id UUID PRIMARY KEY,
    original_url TEXT NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) NOT NULL,
    expires_at TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_shortened_urls_slug ON shortened_urls(slug);

-- URL Visit Operations - Record each visit to a shortened URL
CREATE TABLE url_visit_events (
    visit_id UUID PRIMARY KEY,
    url_id UUID NOT NULL,
    visited_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    referer TEXT,
    device_type VARCHAR(50),
    country_code VARCHAR(2),
    CONSTRAINT fk_url_visits FOREIGN KEY (url_id) REFERENCES shortened_urls(url_id)
);

CREATE INDEX idx_url_visits_url_id ON url_visit_events(url_id);
CREATE INDEX idx_url_visits_visited_at ON url_visit_events(visited_at);

-- Content Analytics Events - Immutable log of content interactions
CREATE TABLE content_analytics_events (
    event_id UUID PRIMARY KEY,
    content_id UUID NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB NOT NULL,
    user_id VARCHAR(100),
    session_id VARCHAR(100),
    ip_address VARCHAR(45),
    user_agent TEXT,
    referer TEXT,
    occurred_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_content_analytics_content FOREIGN KEY (content_id) REFERENCES content_items(content_id)
);

CREATE INDEX idx_content_analytics_content_id ON content_analytics_events(content_id);
CREATE INDEX idx_content_analytics_event_type ON content_analytics_events(event_type);
CREATE INDEX idx_content_analytics_occurred_at ON content_analytics_events(occurred_at);

-- Media Processing Operations - Track media transformations
CREATE TABLE media_processing_operations (
    operation_id UUID PRIMARY KEY,
    media_id UUID NOT NULL,
    operation_type VARCHAR(50) NOT NULL,
    parameters JSONB NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED')),
    result_media_id UUID,
    error_message TEXT,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    requested_by VARCHAR(100) NOT NULL,
    CONSTRAINT fk_media_processing_media FOREIGN KEY (media_id) REFERENCES media_items(media_id),
    CONSTRAINT fk_media_processing_result FOREIGN KEY (result_media_id) REFERENCES media_items(media_id)
);

CREATE INDEX idx_media_processing_media_id ON media_processing_operations(media_id);
CREATE INDEX idx_media_processing_status ON media_processing_operations(status);

-- Content Search Index
CREATE TABLE content_search_entries (
    entry_id UUID PRIMARY KEY,
    content_id UUID NOT NULL,
    title_vector TSVECTOR,
    content_vector TSVECTOR,
    metadata_vector TSVECTOR,
    last_indexed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_content_search_content FOREIGN KEY (content_id) REFERENCES content_items(content_id)
);

CREATE INDEX idx_content_search_content_id ON content_search_entries(content_id);
CREATE INDEX idx_content_search_title_vector ON content_search_entries USING GIN(title_vector);
CREATE INDEX idx_content_search_content_vector ON content_search_entries USING GIN(content_vector);

-- Audit Log - Track all operations performed in the system
CREATE TABLE audit_log (
    log_id UUID PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    action VARCHAR(50) NOT NULL,
    performed_by VARCHAR(100) NOT NULL,
    details JSONB,
    ip_address VARCHAR(45),
    occurred_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_log_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_log_action ON audit_log(action);
CREATE INDEX idx_audit_log_occurred_at ON audit_log(occurred_at);

-- Background Jobs
CREATE TABLE background_jobs (
    job_id UUID PRIMARY KEY,
    job_type VARCHAR(100) NOT NULL,
    parameters JSONB NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('QUEUED', 'RUNNING', 'COMPLETED', 'FAILED')),
    progress SMALLINT CHECK (progress BETWEEN 0 AND 100),
    result JSONB,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_by VARCHAR(100) NOT NULL
);

CREATE INDEX idx_background_jobs_status ON background_jobs(status) WHERE status IN ('QUEUED', 'RUNNING');
CREATE INDEX idx_background_jobs_type ON background_jobs(job_type);

-- Rate Limiting
CREATE TABLE rate_limit_counters (
    counter_id UUID PRIMARY KEY,
    resource_type VARCHAR(50) NOT NULL,
    resource_key VARCHAR(255) NOT NULL,
    counter INT NOT NULL DEFAULT 1,
    window_start TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL
);

CREATE UNIQUE INDEX idx_rate_limit_resource ON rate_limit_counters(resource_type, resource_key, window_start);
CREATE INDEX idx_rate_limit_expires ON rate_limit_counters(expires_at);

-- Feature Flags - Control functionality without code deployment
CREATE TABLE feature_flags (
    flag_name VARCHAR(100) PRIMARY KEY,
    is_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    criteria JSONB,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) NOT NULL,
    updated_by VARCHAR(100) NOT NULL
);

-- Cache Invalidation Events
CREATE TABLE cache_invalidation_events (
    event_id UUID PRIMARY KEY,
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(255) NOT NULL,
    invalidated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cache_invalidation_resource ON cache_invalidation_events(resource_type, resource_id);
CREATE INDEX idx_cache_invalidation_time ON cache_invalidation_events(invalidated_at);

-- Functions for common operations

-- Function to publish content
CREATE OR REPLACE FUNCTION publish_content(
    p_content_id UUID,
    p_channels JSONB,
    p_notify_subscribers BOOLEAN,
    p_performed_by VARCHAR(100)
)
RETURNS UUID AS $$
DECLARE
    v_operation_id UUID;
    v_content_exists BOOLEAN;
BEGIN
    -- Check if content exists and is in draft or scheduled state
    SELECT EXISTS (
        SELECT 1 FROM content_items 
        WHERE content_id = p_content_id 
        AND status IN ('DRAFT', 'SCHEDULED')
    ) INTO v_content_exists;
    
    IF NOT v_content_exists THEN
        RAISE EXCEPTION 'Content not found or not in publishable state';
    END IF;
    
    -- Generate new operation ID
    v_operation_id := gen_random_uuid();
    
    -- Insert publishing operation
    INSERT INTO publishing_operations (
        operation_id, content_id, operation_type, channels, 
        status, notify_subscribers, created_by, execution_time
    ) VALUES (
        v_operation_id, p_content_id, 'PUBLISH', p_channels,
        'COMPLETED', p_notify_subscribers, p_performed_by, CURRENT_TIMESTAMP
    );
    
    -- Update content status
    UPDATE content_items 
    SET status = 'PUBLISHED', 
        updated_at = CURRENT_TIMESTAMP,
        updated_by = p_performed_by
    WHERE content_id = p_content_id;
    
    -- Add audit log entry
    INSERT INTO audit_log (
        log_id, entity_type, entity_id, action, performed_by, details, occurred_at
    ) VALUES (
        gen_random_uuid(), 'CONTENT', p_content_id, 'PUBLISH', p_performed_by,
        jsonb_build_object('channels', p_channels, 'notify_subscribers', p_notify_subscribers),
        CURRENT_TIMESTAMP
    );
    
    -- Create cache invalidation event
    INSERT INTO cache_invalidation_events (
        event_id, resource_type, resource_id, invalidated_at
    ) VALUES (
        gen_random_uuid(), 'CONTENT', p_content_id::TEXT, CURRENT_TIMESTAMP
    );
    
    RETURN v_operation_id;
END;
$$ LANGUAGE plpgsql;

-- Function to add a tag to content
CREATE OR REPLACE FUNCTION tag_content(
    p_content_id UUID,
    p_tag_name VARCHAR(100),
    p_performed_by VARCHAR(100)
)
RETURNS UUID AS $$
DECLARE
    v_operation_id UUID;
BEGIN
    -- Generate new operation ID
    v_operation_id := gen_random_uuid();
    
    -- Insert tagging operation
    INSERT INTO content_tag_operations (
        operation_id, content_id, tag_name, operation_type, performed_by
    ) VALUES (
        v_operation_id, p_content_id, p_tag_name, 'ADD', p_performed_by
    );
    
    -- Add audit log entry
    INSERT INTO audit_log (
        log_id, entity_type, entity_id, action, performed_by, details, occurred_at
    ) VALUES (
        gen_random_uuid(), 'CONTENT', p_content_id, 'ADD_TAG', p_performed_by,
        jsonb_build_object('tag_name', p_tag_name),
        CURRENT_TIMESTAMP
    );
    
    RETURN v_operation_id;
END;
$$ LANGUAGE plpgsql;

-- View to get current content tags (based on operations history)
CREATE OR REPLACE VIEW vw_content_current_tags AS
SELECT 
    content_id,
    tag_name
FROM (
    SELECT 
        content_id,
        tag_name,
        ROW_NUMBER() OVER (
            PARTITION BY content_id, tag_name 
            ORDER BY performed_at DESC
        ) as rn,
        operation_type
    FROM content_tag_operations
) ranked_tags
WHERE 
    rn = 1 AND operation_type = 'ADD';

-- View to get current content categories (based on operations history)
CREATE OR REPLACE VIEW vw_content_current_categories AS
SELECT 
    content_id,
    category_path
FROM (
    SELECT 
        content_id,
        category_path,
        ROW_NUMBER() OVER (
            PARTITION BY content_id, category_path 
            ORDER BY performed_at DESC
        ) as rn,
        operation_type
    FROM content_category_operations
) ranked_categories
WHERE 
    rn = 1 AND operation_type = 'ADD';

-- View for content performance analytics
CREATE OR REPLACE VIEW vw_content_performance_summary AS
SELECT 
    ci.content_id,
    ci.title,
    ci.content_type,
    ci.created_at,
    CASE WHEN ci.status = 'PUBLISHED' THEN
        (SELECT execution_time FROM publishing_operations 
         WHERE content_id = ci.content_id AND operation_type = 'PUBLISH' 
         ORDER BY execution_time DESC LIMIT 1)
    ELSE NULL END AS published_at,
    (SELECT COUNT(*) FROM content_analytics_events 
     WHERE content_id = ci.content_id AND event_type = 'VIEW') AS view_count,
    (SELECT COUNT(DISTINCT session_id) FROM content_analytics_events 
     WHERE content_id = ci.content_id AND event_type = 'VIEW' AND session_id IS NOT NULL) AS unique_view_count,
    (SELECT AVG(CAST(event_data->>'duration_seconds' AS INTEGER)) FROM content_analytics_events 
     WHERE content_id = ci.content_id AND event_type = 'ENGAGEMENT' AND event_data->>'duration_seconds' IS NOT NULL) AS avg_engagement_seconds,
    (SELECT COUNT(*) FROM content_analytics_events 
     WHERE content_id = ci.content_id AND event_type = 'SHARE') AS share_count,
    (SELECT COUNT(*) FROM content_analytics_events 
     WHERE content_id = ci.content_id AND event_type = 'COMMENT') AS comment_count
FROM 
    content_items ci;

-- Trigger function to automatically update search vectors when content changes
CREATE OR REPLACE FUNCTION update_content_search_vectors()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO content_search_entries (
        entry_id, content_id, title_vector, content_vector, metadata_vector
    ) VALUES (
        gen_random_uuid(),
        NEW.content_id,
        to_tsvector('english', COALESCE(NEW.title, '')),
        to_tsvector('english', COALESCE(NEW.content_data->>'text', '')),
        to_tsvector('english', 
            COALESCE(NEW.metadata->>'description', '') || ' ' || 
            COALESCE(NEW.metadata->>'keywords', '')
        )
    )
    ON CONFLICT (content_id) DO UPDATE SET
        title_vector = to_tsvector('english', COALESCE(NEW.title, '')),
        content_vector = to_tsvector('english', COALESCE(NEW.content_data->>'text', '')),
        metadata_vector = to_tsvector('english', 
            COALESCE(NEW.metadata->>'description', '') || ' ' || 
            COALESCE(NEW.metadata->>'keywords', '')
        ),
        last_indexed_at = CURRENT_TIMESTAMP;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger on content items
CREATE TRIGGER trg_update_content_search
AFTER INSERT OR UPDATE OF title, content_data, metadata
ON content_items
FOR EACH ROW
EXECUTE FUNCTION update_content_search_vectors();

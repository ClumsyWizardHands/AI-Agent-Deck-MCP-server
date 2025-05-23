// Empire Builder JavaScript

// Auto-resize textareas
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Initialize auto-resize for all textareas
document.addEventListener('DOMContentLoaded', function() {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', () => autoResizeTextarea(textarea));
        autoResizeTextarea(textarea); // Initial resize
    });
});

// Add new field
function addField(fieldType) {
    const container = document.getElementById(`${fieldType}-container`);
    const fieldGroups = container.querySelectorAll('.field-group');
    
    // Create new field group
    const newFieldGroup = document.createElement('div');
    newFieldGroup.className = 'field-group';
    
    const textarea = document.createElement('textarea');
    textarea.name = `${fieldType}[]`;
    textarea.required = true;
    textarea.placeholder = getPlaceholderForField(fieldType);
    
    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'remove-btn';
    removeBtn.onclick = function() { removeField(this); };
    removeBtn.innerHTML = '×';
    
    newFieldGroup.appendChild(textarea);
    newFieldGroup.appendChild(removeBtn);
    container.appendChild(newFieldGroup);
    
    // Add auto-resize to new textarea
    textarea.addEventListener('input', () => autoResizeTextarea(textarea));
    
    // Update remove button visibility
    updateRemoveButtons(fieldType);
    
    // Focus on new textarea
    textarea.focus();
}

// Remove field
function removeField(button) {
    const fieldGroup = button.parentElement;
    const container = fieldGroup.parentElement;
    const fieldType = container.id.replace('-container', '');
    
    fieldGroup.remove();
    updateRemoveButtons(fieldType);
}

// Update remove button visibility
function updateRemoveButtons(fieldType) {
    const container = document.getElementById(`${fieldType}-container`);
    const fieldGroups = container.querySelectorAll('.field-group');
    
    fieldGroups.forEach((group, index) => {
        const removeBtn = group.querySelector('.remove-btn');
        if (fieldGroups.length > 1) {
            removeBtn.style.display = 'block';
        } else {
            removeBtn.style.display = 'none';
        }
    });
}

// Get placeholder text for field type
function getPlaceholderForField(fieldType) {
    const placeholders = {
        ends: 'Example: Establish durable, AI-literate democratic coalitions...',
        means: 'Example: Empire modeling systems that synthesize relational game theory...',
        principles: 'Example: Narrative Determines Reality: Systems and societies are built on story before law or code...',
        identity: 'Example: I build cognitive infrastructure for coalitions that don\'t realize they\'re already at war...',
        resentments: 'Example: Resentment of AI naiveté among civil society allies...',
        emotions: 'Example: Sorrow for the loss of meaning and memory across digital public spheres...'
    };
    return placeholders[fieldType] || '';
}

// Collect form data
function collectFormData() {
    const formData = {
        empire_name_and_description: document.getElementById('empireNameDescription').value.trim(),
        ends: [],
        means: [],
        principles: [],
        identity: [],
        resentments: [],
        emotions: []
    };
    
    // Collect all field values
    ['ends', 'means', 'principles', 'identity', 'resentments', 'emotions'].forEach(fieldType => {
        const textareas = document.querySelectorAll(`#${fieldType}-container textarea`);
        textareas.forEach(textarea => {
            const value = textarea.value.trim();
            if (value) {
                formData[fieldType].push(value);
            }
        });
    });
    
    return formData;
}

// Display results
function displayResults(agents) {
    console.log('displayResults called with agents:', agents);
    console.log('Number of agents received:', agents ? agents.length : 0);
    
    const resultsContent = document.getElementById('resultsContent');
    resultsContent.innerHTML = '';
    
    if (!agents || agents.length === 0) {
        resultsContent.innerHTML = '<p>No agents were generated. Please try again.</p>';
        return;
    }
    
    // Add summary at the top
    const summary = document.createElement('div');
    summary.style.marginBottom = '20px';
    summary.innerHTML = `<p><strong>Generated ${agents.length} agents</strong></p>`;
    resultsContent.appendChild(summary);
    
    let successCount = 0;
    let errorCount = 0;
    
    agents.forEach((agent, index) => {
        try {
            console.log(`Creating card for agent ${index + 1}:`, agent.agent_name);
            
            const agentCard = document.createElement('div');
            agentCard.className = 'agent-card';
            agentCard.style.animationDelay = `${index * 0.1}s`;
            
            const complexityClass = agent.estimated_complexity_to_build ? agent.estimated_complexity_to_build.toLowerCase() : 'medium';
            
            agentCard.innerHTML = `
                <h3>${agent.agent_name || 'Unnamed Agent'}</h3>
                <div class="agent-id">${agent.agent_id || 'No ID'}</div>
                
                <div class="agent-detail">
                    <strong>Purpose & Tasks:</strong> ${agent.agent_purpose_and_tasks || 'No description'}
                </div>
                
                <div class="agent-detail">
                    <strong>Empire Component:</strong> ${agent.linked_empire_need_or_component || 'Not specified'}
                </div>
                
                <div class="agent-detail">
                    <span class="complexity-badge complexity-${complexityClass}">${agent.estimated_complexity_to_build || 'Medium'}</span>
                </div>
                
                <div class="agent-detail">
                    <strong>Technical Approach:</strong> ${agent.suggested_technical_approach || 'Not specified'}
                </div>
                
                <div class="agent-detail">
                    <strong>Key Inputs:</strong>
                    <ul class="agent-list">
                        ${agent.key_data_inputs && agent.key_data_inputs.length > 0 
                            ? agent.key_data_inputs.map(input => `<li>${input}</li>`).join('')
                            : '<li>None specified</li>'}
                    </ul>
                </div>
                
                <div class="agent-detail">
                    <strong>Key Outputs/Actions:</strong>
                    <ul class="agent-list">
                        ${agent.key_data_outputs_or_actions && agent.key_data_outputs_or_actions.length > 0
                            ? agent.key_data_outputs_or_actions.map(output => `<li>${output}</li>`).join('')
                            : '<li>None specified</li>'}
                    </ul>
                </div>
                
                ${agent.potential_dependencies_or_integrations && agent.potential_dependencies_or_integrations.length > 0 ? `
                <div class="agent-detail">
                    <strong>Dependencies/Integrations:</strong>
                    <ul class="agent-list">
                        ${agent.potential_dependencies_or_integrations.map(dep => `<li>${dep}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}
            `;
            
            resultsContent.appendChild(agentCard);
            successCount++;
            console.log(`Successfully created card ${successCount}`);
        } catch (error) {
            errorCount++;
            console.error(`Error creating card for agent ${index + 1}:`, error);
            console.error('Agent data that caused error:', agent);
            
            // Create error card
            const errorCard = document.createElement('div');
            errorCard.className = 'agent-card';
            errorCard.style.backgroundColor = '#ffeeee';
            errorCard.innerHTML = `
                <h3>Error rendering agent ${index + 1}</h3>
                <p>Error: ${error.message}</p>
                <p>Agent ID: ${agent.agent_id || 'Unknown'}</p>
            `;
            resultsContent.appendChild(errorCard);
        }
    });
    
    console.log(`Display complete. Success: ${successCount}, Errors: ${errorCount}`);
    
    // Check if cards are actually visible
    const cards = resultsContent.querySelectorAll('.agent-card');
    console.log(`Cards found in DOM: ${cards.length}`);
}

// Display error
function displayError(message) {
    const resultsContent = document.getElementById('resultsContent');
    resultsContent.innerHTML = `<div class="error-message">${message}</div>`;
}

// Start new empire
function startNewEmpire() {
    document.getElementById('empireForm').reset();
    document.getElementById('results').style.display = 'none';
    document.getElementById('empireForm').style.display = 'block';
    window.scrollTo(0, 0);
}

// Handle form submission
document.getElementById('empireForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submitBtn');
    const loading = document.getElementById('loading');
    
    // Disable submit button and show loading
    submitBtn.disabled = true;
    loading.style.display = 'flex';
    
    try {
        const formData = collectFormData();
        
        const response = await fetch('/suggest-agents-extended', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `Server error: ${response.status}`);
        }
        
        const agents = await response.json();
        
        console.log('Response received from server:');
        console.log('Type:', typeof agents);
        console.log('Is Array:', Array.isArray(agents));
        console.log('Length:', agents.length);
        console.log('First few agents:', agents.slice(0, 3));
        
        // Hide form and show results
        document.getElementById('empireForm').style.display = 'none';
        document.getElementById('results').style.display = 'block';
        
        displayResults(agents);
        
    } catch (error) {
        console.error('Error:', error);
        
        // Show results section with error
        document.getElementById('empireForm').style.display = 'none';
        document.getElementById('results').style.display = 'block';
        
        displayError(`Error: ${error.message}`);
    } finally {
        // Re-enable submit button and hide loading
        submitBtn.disabled = false;
        loading.style.display = 'none';
    }
});

// Initialize remove button visibility on page load
document.addEventListener('DOMContentLoaded', function() {
    ['ends', 'means', 'principles', 'identity', 'resentments', 'emotions'].forEach(fieldType => {
        updateRemoveButtons(fieldType);
    });
});

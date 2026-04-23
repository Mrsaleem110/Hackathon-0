'use client'

import { useState } from 'react'
import './CommandCenter.css'

export default function CommandCenter() {
  const [chatMessages, setChatMessages] = useState([
    { type: 'bot', text: 'Salam! 👋 AI Employee Vault mein welcome ho. Mujhe instructions do aur main kaam kar dunga!' }
  ])
  const [chatInput, setChatInput] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    taskName: '',
    description: '',
    priority: 'medium',
    platform: 'gmail',
    dueDate: '',
  })
  const [loading, setLoading] = useState(false)

  const handleChatSubmit = async (e) => {
    e.preventDefault()
    if (!chatInput.trim()) return

    // Add user message
    const userMessage = { type: 'user', text: chatInput }
    setChatMessages(prev => [...prev, userMessage])
    setChatInput('')
    setLoading(true)

    try {
      // Send to backend
      const response = await fetch('/api/execute-command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: chatInput })
      })

      const data = await response.json()
      const botMessage = { type: 'bot', text: data.response || 'Command execute ho gaya!' }
      setChatMessages(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage = { type: 'bot', text: '❌ Error: ' + error.message }
      setChatMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleFormSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await fetch('/api/create-task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      const data = await response.json()
      const botMessage = {
        type: 'bot',
        text: `✅ Task create ho gaya!\n\nTask: ${formData.taskName}\nPlatform: ${formData.platform}\nPriority: ${formData.priority}`
      }
      setChatMessages(prev => [...prev, botMessage])

      // Reset form
      setFormData({
        taskName: '',
        description: '',
        priority: 'medium',
        platform: 'gmail',
        dueDate: '',
      })
      setShowForm(false)
    } catch (error) {
      const errorMessage = { type: 'bot', text: '❌ Error: ' + error.message }
      setChatMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <section id="command-center" className="command-center fade-in">
      <div className="command-container">
        <h2 className="section-title">Command Center</h2>
        <p className="command-subtitle">UI ke through instructions do aur AI Employee Vault kaam kar dega</p>

        <div className="command-layout">
          {/* Chat Interface */}
          <div className="chat-section">
            <div className="chat-header">💬 Quick Commands</div>
            <div className="chat-messages">
              {chatMessages.map((msg, idx) => (
                <div key={idx} className={`message ${msg.type}`}>
                  <div className="message-content">{msg.text}</div>
                </div>
              ))}
              {loading && <div className="message bot"><div className="message-content">⏳ Processing...</div></div>}
            </div>
            <form onSubmit={handleChatSubmit} className="chat-form">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder="Instruction likho... (e.g., 'Gmail check karo' ya 'LinkedIn post karo')"
                className="chat-input"
                disabled={loading}
              />
              <button type="submit" className="chat-button" disabled={loading}>
                {loading ? '⏳' : '📤'}
              </button>
            </form>
          </div>

          {/* Task Form */}
          <div className="form-section">
            <button
              className="toggle-form-btn"
              onClick={() => setShowForm(!showForm)}
            >
              {showForm ? '✕ Form Close Karo' : '+ Detailed Task'}
            </button>

            {showForm && (
              <form onSubmit={handleFormSubmit} className="task-form">
                <div className="form-header">📋 Detailed Task Create Karo</div>

                <div className="form-group">
                  <label>Task Name *</label>
                  <input
                    type="text"
                    value={formData.taskName}
                    onChange={(e) => setFormData({...formData, taskName: e.target.value})}
                    placeholder="e.g., Send Invoice to Client A"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    placeholder="Task ki details likho..."
                    rows="3"
                  />
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label>Platform *</label>
                    <select
                      value={formData.platform}
                      onChange={(e) => setFormData({...formData, platform: e.target.value})}
                    >
                      <option value="gmail">📧 Gmail</option>
                      <option value="linkedin">💼 LinkedIn</option>
                      <option value="whatsapp">💬 WhatsApp</option>
                      <option value="instagram">📸 Instagram</option>
                      <option value="facebook">👍 Facebook</option>
                      <option value="twitter">𝕏 Twitter</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Priority</label>
                    <select
                      value={formData.priority}
                      onChange={(e) => setFormData({...formData, priority: e.target.value})}
                    >
                      <option value="low">🟢 Low</option>
                      <option value="medium">🟡 Medium</option>
                      <option value="high">🔴 High</option>
                      <option value="urgent">⚠️ Urgent</option>
                    </select>
                  </div>
                </div>

                <div className="form-group">
                  <label>Due Date</label>
                  <input
                    type="datetime-local"
                    value={formData.dueDate}
                    onChange={(e) => setFormData({...formData, dueDate: e.target.value})}
                  />
                </div>

                <button type="submit" className="form-submit" disabled={loading}>
                  {loading ? '⏳ Creating...' : '✅ Task Create Karo'}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </section>
  )
}

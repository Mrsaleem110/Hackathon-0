'use client'

import './Actions.css'

export default function Actions() {
  return (
    <section id="actions" className="actions-section fade-in">
      <div className="actions-container">
        <h2 className="section-title">Get Started</h2>
        <p className="actions-subtitle">
          Ready to automate your workflow? Choose an action below to begin.
        </p>
        <div className="actions-grid">
          <button className="action-card">
            <div className="action-icon">🚀</div>
            <div className="action-title">Start Orchestrator</div>
            <div className="action-description">Launch the main automation engine</div>
          </button>
          <button className="action-card">
            <div className="action-icon">📊</div>
            <div className="action-title">View Dashboard</div>
            <div className="action-description">Monitor real-time activities</div>
          </button>
          <button className="action-card">
            <div className="action-icon">📋</div>
            <div className="action-title">Check Logs</div>
            <div className="action-description">Review audit trail and history</div>
          </button>
          <button className="action-card">
            <div className="action-icon">📚</div>
            <div className="action-title">Documentation</div>
            <div className="action-description">Learn how to use the system</div>
          </button>
        </div>
      </div>
    </section>
  )
}

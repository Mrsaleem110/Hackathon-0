'use client'

import './Features.css'

export default function Features() {
  const features = [
    {
      icon: '📧',
      title: 'Email Detection',
      description: 'Monitor Gmail for important emails and automatically trigger workflows based on content and sender.',
    },
    {
      icon: '💼',
      title: 'LinkedIn Integration',
      description: 'Post content, track opportunities, and manage professional networking automatically.',
    },
    {
      icon: '📱',
      title: 'WhatsApp Messaging',
      description: 'Send and receive messages through WhatsApp Web with full automation support.',
    },
    {
      icon: '📊',
      title: 'Analytics Dashboard',
      description: 'Real-time insights into all activities, performance metrics, and system health.',
    },
    {
      icon: '🔐',
      title: 'Approval Workflow',
      description: 'Human-in-the-loop approval system for critical actions with audit trail.',
    },
    {
      icon: '⚙️',
      title: 'Smart Orchestration',
      description: 'Intelligent task orchestration with Claude API for context-aware decisions.',
    },
  ]

  return (
    <section id="features" className="features-section fade-in">
      <div className="features-container">
        <h2 className="section-title">Core Features</h2>
        <div className="features-grid">
          {features.map((feature, index) => (
            <div key={index} className="feature-card">
              <div className="feature-icon">{feature.icon}</div>
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

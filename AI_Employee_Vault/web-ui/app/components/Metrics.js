'use client'

import './Metrics.css'

export default function Metrics() {
  const metrics = [
    { value: '99.8%', label: 'Uptime' },
    { value: '245ms', label: 'Avg Response' },
    { value: '0.2%', label: 'Error Rate' },
    { value: '87.4%', label: 'Success Rate' },
  ]

  return (
    <section id="metrics" className="metrics-section fade-in">
      <div className="metrics-container">
        <h2 className="section-title">System Metrics</h2>
        <div className="metrics-grid">
          {metrics.map((metric, index) => (
            <div key={index} className="metric">
              <div className="metric-value">{metric.value}</div>
              <div className="metric-label">{metric.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

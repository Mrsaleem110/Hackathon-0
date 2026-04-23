'use client'

import './Stats.css'

export default function Stats({ stats }) {
  return (
    <section className="stats-section fade-in">
      <div className="stats-container">
        <div className="stat-card">
          <div className="stat-number">{stats.platforms}</div>
          <div className="stat-label">Platforms Connected</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{stats.actions}</div>
          <div className="stat-label">Actions Logged</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{stats.successRate}%</div>
          <div className="stat-label">Success Rate</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{stats.uptime}%</div>
          <div className="stat-label">Uptime</div>
        </div>
      </div>
    </section>
  )
}

'use client'

import { useState, useEffect } from 'react'
import Header from './components/Header'
import Hero from './components/Hero'
import Stats from './components/Stats'
import Features from './components/Features'
import Platforms from './components/Platforms'
import Metrics from './components/Metrics'
import CommandCenter from './components/CommandCenter'
import Actions from './components/Actions'
import Footer from './components/Footer'
import './page.css'

export default function HomeClient() {
  const [stats, setStats] = useState({
    platforms: 6,
    actions: 247,
    successRate: 87.4,
    uptime: 99.8,
  })
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    // Fetch real stats from API if available
    const fetchStats = async () => {
      try {
        const response = await fetch('/api/stats')
        if (response.ok) {
          const data = await response.json()
          setStats(data)
        }
      } catch (error) {
        console.log('Using default stats')
      }
    }

    fetchStats()
  }, [])

  if (!mounted) {
    return null
  }

  return (
    <main className="main-container">
      <Header />
      <Hero />
      <Stats stats={stats} />
      <Features />
      <Platforms />
      <Metrics />
      <CommandCenter />
      <Actions />
      <Footer />
    </main>
  )
}


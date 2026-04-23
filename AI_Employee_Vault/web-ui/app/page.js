import dynamic from 'next/dynamic'

const HomeClient = dynamic(() => import('./home-client'), {
  ssr: true,
})

export const metadata = {
  title: 'AI Employee Vault',
  description: 'Intelligent Multi-Channel Communication & Automation Platform',
}

export default function Home() {
  return <HomeClient />
}

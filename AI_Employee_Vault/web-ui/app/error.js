'use client'

export default function Error({ error, reset }) {
  return (
    <div style={{ padding: '40px', textAlign: 'center' }}>
      <h1>500 - Server Error</h1>
      <p>Something went wrong.</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}

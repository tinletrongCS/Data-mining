import { NavLink } from 'react-router-dom'

const navItems = [
  { to: '/overview',   icon: '📊', label: 'Tổng quan' },
  { to: '/temporal',   icon: '📅', label: 'Thời gian' },
  { to: '/clustering', icon: '🔮', label: 'Phân cụm' },
  { to: '/comparison', icon: '⚖️', label: 'So sánh' },
  { to: '/association-rules', icon: '🛒', label: 'Luật kết hợp' }, // <-- Thêm dòng này
]

export default function Navbar() {
  return (
    <nav className="sidebar">
      <div className="nav-logo">
        <h2>💎 DataMining</h2>
        <p>Jewelry Analytics</p>
      </div>

      <div className="nav-section">Phân tích</div>

      {navItems.map(item => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
        >
          <span className="nav-icon">{item.icon}</span>
          <span>{item.label}</span>
        </NavLink>
      ))}

      <div className="nav-footer">
        <div>Dataset</div>
        <span>Jewelry E-Commerce</span>
        <div>Dec 2018 - Dec 2021</div>
        <div style={{ marginTop: 6 }}>Model</div>
        <span>KMeans (K=4)</span><br />

        <span>Apriori</span><br />

        <span>FP-Growth</span><br />
      </div>
    </nav>
  )
}

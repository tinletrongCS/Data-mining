import React from 'react';
import ChartCard from '../components/ChartCard';
import StatCard from '../components/StatCard';
import rulesData from '../data/rules_data.json';

export default function AssociationRulesPage() {
  const { benchmark, top_rules_standard, top_rules_super } = rulesData;

  // Render bảng luật kết hợp
  const renderRulesTable = (rules) => (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', textAlign: 'left' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', color: '#94a3b8' }}>
            <th style={{ padding: '12px' }}>Sản phẩm A (Antecedents)</th>
            <th style={{ padding: '12px' }}>Sản phẩm B (Consequents)</th>
            <th style={{ padding: '12px' }}>Support</th>
            <th style={{ padding: '12px' }}>Confidence</th>
            <th style={{ padding: '12px', color: '#00d4ff' }}>Lift</th>
          </tr>
        </thead>
        <tbody>
          {rules.map((rule, idx) => (
            <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
              <td style={{ padding: '12px', color: '#e2e8f0', fontWeight: '500' }}>{rule.antecedents}</td>
              <td style={{ padding: '12px', color: '#e2e8f0', fontWeight: '500' }}>{rule.consequents}</td>
              <td style={{ padding: '12px' }}>{(rule.support * 100).toFixed(2)}%</td>
              <td style={{ padding: '12px' }}>{(rule.confidence * 100).toFixed(2)}%</td>
              <td style={{ padding: '12px', color: '#00d4ff', fontWeight: 'bold' }}>{rule.lift.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  return (
    <div className="fade-up">
      <div className="page-header">
        <h1>🛒 Luật kết hợp</h1>
        <p>Khai phá luật kết hợp, So sánh hiệu năng thuật toán Apriori với FP-Growth và Tối ưu thuật toán FP-Growth bằng Ngưỡng hỗ trợ đa trị </p>
      </div>

      {/* So sánh hiệu năng hai thuật toán */}
      <h3 style={{ marginBottom: '16px', color: '#e2e8f0' }}>⚖️ So sánh tài nguyên và hiệu năng</h3>
      <div className="charts-grid grid-2" style={{ marginBottom: '32px' }}>
        <ChartCard title="Thuật toán Apriori" badge="Truyền thống">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '10px' }}>
            <div className="cluster-stat">Thời gian chạy <span>{benchmark.apriori.time_sec} giây</span></div>
            <div className="cluster-stat">Tiêu thụ RAM <span>{benchmark.apriori.memory_mb} MB</span></div>
            <div className="cluster-stat">Tập phổ biến sinh ra <span>{benchmark.apriori.itemsets}</span></div>
            <div className="cluster-stat">Luật kết hợp tạo ra <span>{benchmark.apriori.rules}</span></div>
          </div>
        </ChartCard>

        <ChartCard title="Thuật toán FP-Growth" badge="Truyền thống">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '10px' }}>
            <div className="cluster-stat">Thời gian chạy <span style={{color: '#fb0000'}}>{benchmark.fpgrowth.time_sec} giây</span></div>
            <div className="cluster-stat">Tiêu thụ RAM <span style={{color: '#22c55e'}}>{benchmark.fpgrowth.memory_mb} MB</span></div>
            <div className="cluster-stat">Tập phổ biến sinh ra <span>{benchmark.fpgrowth.itemsets}</span></div>
            <div className="cluster-stat">Luật kết hợp tạo ra <span>{benchmark.fpgrowth.rules}</span></div>
          </div>
        </ChartCard>
      </div>

      {/* Các luật khám phá được */}
      <div className="charts-grid">
        

        <ChartCard 
          title="Top Luật Kết Hợp Tốt Nhất (FP-Growth Truyền thống)" 
        >
          {renderRulesTable(top_rules_standard)}
        </ChartCard>

        <ChartCard title="FP-Growth Tối ưu" badge="Tối ưu" style={{ border: '1px solid #3b82f6' }}>
          <div className="cluster-info">
            <div className="cluster-stat">Thời gian chạy <span style={{color: '#fe0000'}}>{benchmark.fpgrowth_super.time_sec}s</span></div>
            <div className="cluster-stat">Tiêu thụ RAM <span style={{color: '#fe0000'}}>{benchmark.fpgrowth_super.memory_mb} MB</span></div>
            <div className="cluster-stat">Tập phổ biến sinh ra<span style={{fontWeight: 'bold'}}>{benchmark.fpgrowth_super.itemsets}</span></div>
            <div className="cluster-stat">Luật kết hợp tạo ra <span style={{fontWeight: 'bold', color: '#00d4ff'}}>{benchmark.fpgrowth_super.rules}</span></div>
          </div>
        </ChartCard>

        <ChartCard 
          title="Top Luật Kết Hợp Tốt Nhất (FP-Growth Tối ưu)" 
          badge="Tối ưu"
        >
          {renderRulesTable(top_rules_super)}
        </ChartCard>
        

      </div>


    </div>
  );
}
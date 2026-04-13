import React, { useMemo } from 'react';
import ChartCard from '../components/ChartCard';
import CorrelationHeatmap from '../components/charts/CorrelationHeatmap';
import { correlationData } from '../data/mockData';

export default function ComparisonPage() {
  // Logic tự động tìm Top 4 cặp có độ tương quan mạnh nhất
  const topCorrelations = useMemo(() => {
    if (!correlationData || !correlationData.matrix) return [];
    
    const labels = correlationData.labels;
    const matrix = correlationData.matrix;
    const pairs = [];
    
    for (let i = 0; i < labels.length; i++) {
      for (let j = i + 1; j < labels.length; j++) {
        pairs.push({
          pair: `${labels[i]} ↔ ${labels[j]}`,
          val: Number(matrix[i][j]),
          absVal: Math.abs(matrix[i][j])
        });
      }
    }
    
    pairs.sort((a, b) => b.absVal - a.absVal);
    
    // Đã khắc phục lỗi xét điều kiện p = 0
    return pairs.slice(0, 4).map(p => {
      let note = '';
      if (p.val > 0) {
        note = 'Tương quan thuận: Yếu tố này tăng thì yếu tố kia cũng có xu hướng tăng.';
      } else if (p.val < 0) {
        note = 'Tương quan nghịch: Hai yếu tố có xu hướng ngược chiều nhau.';
      } else {
        note = 'Độc lập: Hai biến số này không có sự tương quan tuyến tính.';
      }

      return {
        pair: p.pair,
        val: p.val.toFixed(2),
        note: note
      };
    });
  }, []);

  return (
    <div className="fade-up">
      <div className="page-header">
        <h1>⚖️ So sánh & Phân tích tương quan</h1>
        <p>Tiền xử lý dữ liệu và ma trận tương quan giữa các biến số</p>
      </div>

      <div className="charts-grid">

        <ChartCard
          title="So sánh trước và sau tiền xử lý"
          subtitle="Phân phối giá sản phẩm tiệm cận phân phối chuẩn sau khi Log Transform"
          badge="Preprocessing"
        >
          {/* ĐÃ THAY BIỂU ĐỒ BẰNG HÌNH ẢNH */}
          <div style={{ width: '100%', display: 'flex', justifyContent: 'center', marginBottom: '16px' }}>
            <img 
              src="/images/preprocessing_comparison.png" 
              alt="So sánh trước và sau tiền xử lý" 
              style={{ maxWidth: '100%', height: 'auto', borderRadius: '8px', objectFit: 'contain' }}
            />
          </div>
          
          {/* THÊM KHỐI INSIGHT NÀY VÀO NGAY DƯỚI BIỂU ĐỒ
          <div style={{ marginTop: 16, padding: '12px 14px', background: 'rgba(245, 158, 11, 0.08)', borderRadius: 6, borderLeft: '4px solid #f59e0b', fontSize: 13, color: '#cbd5e1', lineHeight: 1.6 }}>
            <strong style={{ color: '#f59e0b' }}>💡 Insight phân tích:</strong> Đường cong tiệm cận phân phối chuẩn (Bell Curve) này được thể hiện rõ nhất là nhờ kỹ thuật <strong>"Zoom" giới hạn vùng giá &lt; $1979</strong> (Cắt tỉa phân vị 99.9%). Nếu giữ lại 0.1% các mặt hàng xa xỉ có giá cực cao, biểu đồ sẽ bị kéo lệch phải (Right-skewed) rất mạnh, khiến K-Means bị thiên lệch tâm cụm.
          </div> */}

          {/* Khối quy trình xử lý cũ giữ nguyên */}
          <div style={{ marginTop: 14, padding: '12px 16px', background: 'rgba(0,212,255,0.05)', borderRadius: 8, border: '1px solid rgba(0,212,255,0.15)', fontSize: 12, color: '#94a3b8', lineHeight: 1.7 }}>
            <strong style={{ color: '#00d4ff' }}>Quy trình xử lý:</strong>
            <ul style={{ paddingLeft: 18, marginTop: 6 }}>
              <li>Làm sạch cơ bản và Xử lý dữ liệu thiếu</li>
              <li>Xử lý nhiễu và ngoại lai</li>
              <li>Kỹ thuật đặc trưng và Rời rạc hóa (Binning)</li>
              <li>Mã hóa và Chuẩn hóa</li>
            </ul>
          </div>
        </ChartCard>

        <ChartCard
          title="Top Ma trận tương quan (Insights)"
          // subtitle="Được trích xuất tự động từ thuật toán Pearson"
          badge="Dynamic Heatmap"
        >
          <CorrelationHeatmap />
          
          <div style={{ marginTop: 14, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            {topCorrelations.map(item => (
              <div key={item.pair} style={{ padding: '10px 12px', background: 'rgba(255,255,255,0.03)', borderRadius: 8, border: '1px solid rgba(255,255,255,0.06)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                  <span style={{ color: '#e2e8f0', fontWeight: 500, fontSize: 13 }}>{item.pair}</span>
                  <span style={{ 
                    color: item.val > 0 ? '#ff2626' : (item.val < 0 ? '#0068fa' : '#94a3b8'), 
                    fontWeight: 'bold' 
                  }}>
                    {item.val}
                  </span>
                </div>
                <div style={{ color: '#94a3b8', fontSize: 12 }}>{item.note}</div>
              </div>
            ))}
          </div>
        </ChartCard>
      </div>
    </div>
  );
}
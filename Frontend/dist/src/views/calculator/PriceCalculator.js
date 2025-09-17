import React, { useState, useEffect } from 'react';

const PriceCalculator = () => {
  const [classLevel, setClassLevel] = useState('');
  const [originalPrice, setOriginalPrice] = useState('');
  const [discount, setDiscount] = useState('');
  const [finalPrice, setFinalPrice] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    if (originalPrice && discount) {
      const price = parseFloat(originalPrice);
      const discountPercent = parseFloat(discount);
      if (!isNaN(price) && !isNaN(discountPercent)) {
        const discountAmount = price * (discountPercent / 100);
        const calculatedPrice = price - discountAmount;
        setFinalPrice(calculatedPrice.toFixed(2));
      } else {
        setFinalPrice(null);
      }
    } else {
      setFinalPrice(null);
    }
  }, [originalPrice, discount]);

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!classLevel || !originalPrice || !discount || !finalPrice) {
      setError('Please fill in all fields correctly.');
      return;
    }

    alert(
      `Class: ${classLevel}\nOriginal Price: ₹${originalPrice}\nDiscount: ${discount}%\nFinal Price: ₹${finalPrice}`
    );

    setSuccess('Data ready to be submitted!');

    setClassLevel('');
    setOriginalPrice('');
    setDiscount('');
    setFinalPrice(null);
  };

  return (
    <div className="px-2">
      <h2 className="mb-3 fw-bold text-center">Price Calculator</h2>

      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <div style={{ maxWidth: '450px' }}>
        <div className="mb-2">
          <label className="form-label fw-bold">Class</label>
          <select
            className="form-select"
            value={classLevel}
            onChange={(e) => setClassLevel(e.target.value)}
          >
            <option value="">Select Class</option>
            {[6, 7, 8, 9, 10].map((cls) => (
              <option key={cls} value={cls}>
                Class {cls}
              </option>
            ))}
          </select>
        </div>

        <div className="mb-2">
          <label className="form-label fw-bold">Original Price (₹)</label>
          <input
            type="number"
            className="form-control"
            value={originalPrice}
            onChange={(e) => setOriginalPrice(e.target.value)}
            placeholder="Enter original price"
            min="0"
            step="0.01"
          />
        </div>

        <div className="mb-2">
          <label className="form-label fw-bold">Discount (%)</label>
          <input
            type="number"
            className="form-control"
            value={discount}
            onChange={(e) => setDiscount(e.target.value)}
            placeholder="Enter discount percentage"
            min="0"
            max="100"
            step="0.01"
          />
        </div>

        <div className="mb-2">
          <label className="form-label fw-bold">Final Price (₹)</label>
          <input
          type="text"
          className="form-control price-calculator-input" 
          value={finalPrice ? `₹${finalPrice}` : ''}
          readOnly
         placeholder="Final price will be calculated"
         />

        </div>

        <button type="button" onClick={handleSubmit} className="btn btn-primary w-100 mt-2">
          Submit
        </button>
      </div>
    </div>
  );
};

export default PriceCalculator;

import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Select from "react-select";
import {
  setClassLevel,
  setOriginalPrice,
  setDiscount,
  reset,
  fetchCalculatePrice,
  fetchClassList,
} from "../../redux/calculatorSlice";

const PriceCalculator = () => {
  const dispatch = useDispatch();
  const {
    classLevel,
    classList,
    originalPrice,
    discount,
    finalPrice,
    error,
    success,
    loading,
  } = useSelector((state) => state.calculator);

  const [previewPrice, setPreviewPrice] = useState("");
  const [warning, setWarning] = useState("");

  useEffect(() => {
    dispatch(fetchClassList());
  }, [dispatch]);

  useEffect(() => {
    const priceNum = parseFloat(originalPrice);
    const discountNum = parseFloat(discount);

    if (!isNaN(priceNum) && !isNaN(discountNum)) {
      const calcPrice =
        Math.round((priceNum - priceNum * (discountNum / 100) + Number.EPSILON) * 100) / 100;
      setPreviewPrice(calcPrice.toFixed(2));
    } else {
      setPreviewPrice("");
    }
  }, [originalPrice, discount]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!classLevel || !originalPrice || !discount) {
      setWarning("⚠ Please fill out all the fields.");
      return;
    }
    setWarning("");

    dispatch(
      fetchCalculatePrice({
        class_id: parseInt(classLevel, 10), 
        original_price: parseFloat(originalPrice),
        discount_percentage: parseFloat(discount),
        final_price: parseFloat(previewPrice),
      })
    );
  };

  useEffect(() => {
    if (success || error || warning) {
      const timer = setTimeout(() => {
        dispatch(reset());
        setWarning("");
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [success, error, warning, dispatch]);

  return (
    <div className="px-2 price-calculator">
      <h2
        className="mt-0 mb-2 text-center"
        style={{
          fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
          fontWeight: 700,
          fontSize: "2.3rem",
          letterSpacing: "0.5px",
        }}
      >
        Price Calculator
      </h2>

      {(warning || success || error) && (
        <div
          className={`mx-auto mb-1 p-1 text-center fw-bold rounded ${
            warning
              ? "bg-light-warning text-dark"
              : success
              ? "bg-light-success text-white"
              : "bg-light-danger text-white"
          }`}
          style={{ maxWidth: "600px" }}
        >
          {warning ||
            (success ? "✅ Data Calculated successfully!" : `❌ ${error}`)}
        </div>
      )}

      <div style={{ width: "100%", display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div className="mb-3 class-field-wrapper" style={{ maxWidth: "700px", width: "100%" }}>
           <label className="form-label fs-6 fw-bold">Class</label>
          <Select
          classNamePrefix="select"
          options={classList.map((cls) => ({
          value: cls.id,
          label: cls.name,
        }))}
          value={
         classList
         .map((cls) => ({ value: cls.id, label: cls.name }))
         .find((option) => option.value === classLevel) || null
        }
       onChange={(option) => dispatch(setClassLevel(option?.value))}
       placeholder="Select Class"
       isSearchable={false} 
       noOptionsMessage={() => "Loading classes..."}
      />
        </div>

        <div className="mb-3" style={{ maxWidth: "700px", width: "100%" }}>
          <label className="form-label fs-6 fw-bold mt-0">Original Price (₹)</label>
          <input
           type="text"
           className="form-control price-calculator-field"
           value={originalPrice}
           onChange={(e) => {
           const value = e.target.value;
           if (/^\d*\.?\d*$/.test(value)) {
           dispatch(setOriginalPrice(value));
          }
        }}
          placeholder="Enter original price"
       />
        </div>

        <div className="mb-3" style={{ maxWidth: "700px", width: "100%" }}>
          <label className="form-label fs-6 fw-bold">Discount (%)</label>
         <input
          type="text"
          className="form-control price-calculator-field"
          value={discount}
          onChange={(e) => {
          const value = e.target.value;
          if (/^\d*\.?\d*$/.test(value)) {
          dispatch(setDiscount(value));
        }
        }}
        placeholder="Enter discount percentage"
        />

        </div>

        <div className="mb-3" style={{ maxWidth: "700px", width: "100%" }}>
          <label className="form-label fs-6 fw-bold">Final Price (₹)</label>
          <input
            type="text"
            className="form-control price-calculator-field"
            value={previewPrice ? `₹${previewPrice}` : ""}
            readOnly
            placeholder="Final price will be shown"
            style={{ backgroundColor: "#f9f9f9" }}
          />
        </div>
        <button
          type="button"
          onClick={handleSubmit}
          className="btn btn-primary mb-0"
          disabled={loading}
          style={{ padding: "0.9rem", maxWidth: "300px", width: "100%" }}
        >
          {loading ? "Submit" : "Submit"}
        </button>
      </div>
    </div>
  );
};

export default PriceCalculator;   

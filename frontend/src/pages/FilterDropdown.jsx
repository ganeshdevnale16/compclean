import { useState, useRef, useEffect } from "react";

function FilterDropdown({ label, options, selected, setSelected }) {

  const [open, setOpen] = useState(false);
  const ref = useRef();

  const toggle = (value) => {
    if (selected.includes(value)) {
      setSelected(selected.filter(v => v !== value));
    } else {
      setSelected([...selected, value]);
    }
  };

  const selectAll = () => setSelected(options);
  const clearAll = () => setSelected([]);

  useEffect(() => {
    const close = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, []);

  return (
    <div className="filter-box" ref={ref}>

      <label>{label}</label>

      <div className="dropdown-input" onClick={()=>setOpen(!open)}>
        {selected.length ? `${selected.length} selected` : "Select"}
      </div>

      {open && (
        <div className="dropdown-menu">

          <div className="dropdown-actions">
            <span onClick={selectAll}>Select All</span>
            <span onClick={clearAll}>Clear</span>
          </div>

          {options.map(opt => (
            <label key={opt} className="dropdown-item">
              <input
                type="checkbox"
                checked={selected.includes(opt)}
                onChange={()=>toggle(opt)}
              />
              {opt}
            </label>
          ))}

        </div>
      )}

    </div>
  );
}

export default FilterDropdown;
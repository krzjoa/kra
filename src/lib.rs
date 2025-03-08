use polars::prelude::*;
use pyo3_polars::PySeries;
use pyo3::{
    pymodule,
    types::{PyModule},
    PyResult, Python
};

use std::collections::HashMap;


fn encode_labels_(series: Series) -> Result<Series, PolarsError>{

    let mut values_map: HashMap<&str, series.> = HashMap::new();
    let mut last_idx: u32 = 0;
    let mut vector = vec![last_idx; series.len()];

    // for idx, val in series.into_iter().enumerate() {
    //     values_map.try_insert()
    // }

    Ok(Series::new(&"output", vector))
}



#[pymodule]
fn kra<'py>(_py: Python<'py>, m: &'py PyModule) -> PyResult<()> {

    fn encode_labels(py_series: PySeries) -> Series{
        let series: Series = py_series.into();
        encode_labels_(series).unwrap()
    }

    #[pyfn(m)]
    #[pyo3(name = "encode_labels")]
    fn encode_labels_py<'py>(
        py_series: PySeries
    ) -> PyResult<PySeries> {
        Ok(PySeries(encode_labels(py_series)))
    }

    Ok(())
}
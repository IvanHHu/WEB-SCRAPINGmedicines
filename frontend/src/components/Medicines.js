import React, {useState, useEffect} from 'react'
import {SearchBD} from './SearchBD'


const API = process.env.REACT_APP_API;
export const Medicines = () =>{

    
    const [medicines, setMedicines] = useState([])

    const getMedicines = async() => {
        const res = await fetch(`${API}/get_medicines`)
        const data = await res.json();
        setMedicines(data)
    }

    useEffect(() => {
        getMedicines();

    }, [])


    return (
        <div>
            <SearchBD/>

            <br></br> 
            <br></br>
            <h2> Registros </h2>
            <table className = "table table-striped">
                <thead >
                    <tr>
                        <th> <h5> #</h5></th>
                        <th><h5>Medicamento</h5> </th>
                        <th> <h5> Generico</h5></th>
                        <th> <h5> Operaciones </h5></th>
                    </tr>
                </thead>
                <tbody>
                {medicines.map(medicine => (
                    <tr key = {medicine.id}>
                        <td> {medicine.id} </td>
                        <td> {medicine.producto} </td>
                        <td> {medicine.generico} </td>
                        <td>  <input type="submit"  onClick={() => this.sendMedicamento(medicine.producto)} className ="btn btn-lg btn-info btn-block" value="Buscar en farmacias"/> </td>
                    </tr>
                ))}
                </tbody>
            </table>

        </div>

    )
}
import React, {useState, useEffect} from 'react'
import {SearchBD} from './SearchBD'
import { SearchPre } from './SearchPre';


const API = process.env.REACT_APP_API;
export const Medicines = () =>{

    
    const [medicines, setMedicines] = useState([])

    const getMedicines = async() => {
        const res = await fetch(`${API}/get_last_medicines`)
        const data = await res.json();
        setMedicines(data)
    }

    useEffect(() => {
        getMedicines();

    }, [])


    return (
        <div>
            <SearchPre/>

            <br></br> 
            <br></br>
            <br></br> 
            <br></br>
            <h2> Ultimos medicamentos agregados </h2>
            <table className = "table table-striped">
                <thead >
                    <tr>
                        <th> <h5> #</h5></th>
                        <th><h5>Medicamento</h5> </th>
                        <th> <h5> Generico</h5></th>
                    </tr>
                </thead>
                <tbody>
                {medicines.map(medicine => (
                    <tr key = {medicine.id}>
                        <td> {medicine.id} </td>
                        <td> {medicine.producto} </td>
                        <td> {medicine.generico} </td>
                        </tr>
                ))}
                </tbody>
            </table>

        </div>

    )
}
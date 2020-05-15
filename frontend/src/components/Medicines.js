import React, {useState, useEffect} from 'react'


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

        <div className="col-md-10"> 
        <h2> Registros </h2>
            <table className = "table table-striped">
                <thead >
                    <tr>
                        <th># </th>
                        <th>Medicamento </th>
                        <th>Generico </th>
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
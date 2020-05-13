import React, {useState, useEffect} from 'react'


const API = process.env.REACT_APP_API;
export const Medicines = () =>{

    const [medicine, setMedicine] = useState('')
    const [medicines, setMedicines] = useState([])

    const handleSubmit = async (e) =>{
        e.preventDefault();
        const res = await fetch(`${API}/cafam/`+ medicine , {
            method: 'POST',
            mode: 'cors'
        })
        const data = await res.json();
        console.log(data)
    }

    const getMedicines = async() => {
        const res = await fetch(`${API}/get_medicines`)
        const data = await res.json();
        setMedicines(data)
    }

    useEffect(() => {
        getMedicines();

    }, [])


    return (
        <div className="row">
            <div className="col-md-12">
                <form onSubmit={handleSubmit} className="card card-body">
                    <div className = "form-group">
                        <input type="text" onChange={e => setMedicine(e.target.value)} 
                            value = {medicine}
                            className="form-control"
                            placeholder= "Medicine"
                            autofocus
                        />
                        <div class="text-right container p-2"  >
                            <button className= "btn btn-primary"  >
                                Search
                            </button>
                        </div>
                        
                    </div> 
                   
                    
                    
                </form>
            </div>
            <div className="col-md-6"> 
                <table className = "table table-striped">
                    <thead>
                        <tr>
                            <th>Medicamento </th>
                            <th>Generico </th>
                        </tr>
                    </thead>
                    <tbody>

                    {medicines.map(medicine => (
                        <tr key = {medicine.id}>
                            <td> {medicine.producto} </td>
                            <td> {medicine.generico} </td>

                        </tr>

                    ))}

                    </tbody>
                </table>
            </div>
        </div>
    )
}
import React, {useState, useEffect} from 'react'
import {SearchBD} from './SearchBD'
import { Pagination } from './Pagination'
import { SearchPre } from './SearchPre';


const API = process.env.REACT_APP_API;
export const Catalogo = () =>{

    
    const [medicines, setMedicines] = useState([]);
    const [loading, setLoading ] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [medicinesPerPage ] = useState(1000);



    const getMedicines = async() => {
        const res = await fetch(`${API}/get_medicines`)
        const data = await res.json();
        console.log(data)
        setMedicines(data)
        setLoading(false)

    }

    useEffect(() => {
        getMedicines();

    }, [])

    if (loading) {
        return <h2> Loading...  </h2>
    }

    
    //get current posts
    const indexOfLastPost = currentPage * medicinesPerPage;
    const indexOfFirstPost = indexOfLastPost - medicinesPerPage;
    const currentMedicines = medicines.slice( indexOfFirstPost, indexOfLastPost );

    // change page
    const paginate = pageNumber => setCurrentPage(pageNumber)

    return (
        <div>
            
            <h2> Medicamentos  </h2>
            <table className = "table table-striped">
                <thead >
                    <tr>
                        <th> <h5> #</h5></th>
                        <th><h5>Medicamento</h5> </th>
                        <th> <h5> Generico</h5></th>
                    </tr>
                </thead>
                <tbody>
                {currentMedicines.map(medicine => (
                    <tr key = {medicine.id}>
                        <td> {medicine.id} </td>
                        <td> {medicine.producto} </td>
                        <td> {medicine.generico} </td>
                        </tr>
                ))}
                
                </tbody>
            </table>

            <Pagination 
            medicinesPerPage = {medicinesPerPage} 
            totalMedicines = {medicines.length}
            paginate = {paginate}

             />

        </div>

    )
}
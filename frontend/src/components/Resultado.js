import React, {Component} from 'react';

export class Resultado extends Component{
    mostrarMedicines = () => {
        const medicines = this.props.medicines;
        const medicinesCV = this.props.medicinesCV;
        const medicinesLC = this.props.medicinesLC;


        if (medicines.length === 0) return  null;
        if (medicinesCV.length === 0) return  null;
        if (medicinesLC.length === 0) return  null;

        console.log(medicines);
        console.log(medicinesCV);
        console.log(medicinesLC);
        return(
            <React.Fragment>
                <div className="col-12 p5 row">
                    <table className = "table table-striped">
                    <thead >
                        <h4>Resultados de Cafam</h4>
                        <tr>
                            <th>Medicamento </th>
                            <th>Precio </th>
                        </tr>
                    </thead>
                    <tbody>
                    {medicines.map(medicine => (
                        <tr key = {medicine.medicamento }>
                            <td> {medicine.medicamento} </td>
                            <td> {medicine.precio} </td>

                        </tr>
                    ))}
                    </tbody>
                    </table>
                </div>

                <div className="col-12 p5 row">
                    <table className = "table table-striped">
                    <thead >
                        <h4>Resultados de Cruz Verde</h4>
                        <tr>
                            <th>Medicamento </th>
                            <th>Precio </th>
                        </tr>
                    </thead>
                    <tbody>
                    {medicinesCV.map(medicineCV => (
                        <tr key = {medicineCV.medicamento }>
                            <td> {medicineCV.medicamento} </td>
                            <td> {medicineCV.precio} </td>

                        </tr>
                    ))}
                    </tbody>
                    </table>
                </div>

                <div className="col-12 p5 row">
                    <table className = "table table-striped">
                    <thead >
                        <h4>Resultados de Locatel</h4>
                        <tr>
                            <th>Medicamento </th>
                            <th>Precio </th>
                        </tr>
                    </thead>
                    <tbody>
                    {medicinesLC.map(medicineLC => (
                        <tr key = {medicineLC.medicamento }>
                            <td> {medicineLC.medicamento} </td>
                            <td> {medicineLC.precio} </td>

                        </tr>
                    ))}
                    </tbody>
                    </table>
                </div>
            </React.Fragment>
        )
    }



    render(){
        return(
            <React.Fragment>
                { this.mostrarMedicines() }
            </React.Fragment>
                 
        )
    }

}

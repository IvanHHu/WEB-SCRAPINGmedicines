import React, {Component} from 'react';

export class ResultadoFull extends Component{
    mostrarMedicines = () => {
        const medicines = this.props.medicines;
        const genericos = this.props.genericos;

        const medicinesCV = this.props.medicinesCV;
        const genericosCV = this.props.genericosCV;

        const medicinesLC = this.props.medicinesLC;
        const genericosLC = this.props.genericosLC;

        const wiki = this.props.wiki

    
        if (medicines.length === 0) return  null;

        if (genericos.length === 0) return  null;

        if (medicinesCV.length === 0) return  null;

        if (genericosCV.length === 0) return  null;

        if (medicinesLC.length === 0) return  null;

        if (genericosLC.length === 0) return  null;

        if (wiki.length === 0) return  null;


        //console.log(medicines);
        //console.log(genericos);

        //console.log(medicinesCV);
        //console.log(genericosCV);

        //console.log(medicinesLC);
        //console.log(genericosLC);
        console.log(wiki);

        return(
            <React.Fragment>
                <div className="col-12  ">
                    <table className = "table table-striped card card-body">
                    <thead >
                        <tr>
                            <th>Descripcion de Wikipedia </th>
                        </tr>
                    </thead>
                    <tbody>
                    {wiki.map(wik => (
                        <tr key = {wik.medicamento }>
                            <td> {wik.descripcion} </td>
                        </tr>
                    ))}
                    </tbody>
                    </table>
                </div>


                <div className="col-12 col-sm-6 col-md-6 col-lg-6 mb4 ">
                <h6 >Medicamentos de Cafam</h6>
                    <table className = "table table-striped card card-body">
                    <thead >
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

                <div className="col-12 col-sm-6 col-md-6 col-lg-6 mb4 ">
                <h6 >Genericos de Cafam</h6>
                    <table className = "table table-striped card card-body">
                    <thead >
                        <tr>
                            <th>Generico </th>
                            <th>Precio </th>
                            
                        </tr>
                    </thead>
                    <tbody>
                    {genericos.map(generico => (
                        <tr key = {generico.medicamento }>
                            <td> {generico.medicamento} </td>
                            <td> {generico.precio} </td>

                        </tr>
                    ))}
                    </tbody>
                    </table>
                </div>

                <div className="col-12 col-sm-6 col-md-6 col-lg-6 mb4 ">
                <h6 >Medicamentos de Cruz Verde</h6>
                    <table className = "table table-striped card card-body">
                    <thead >
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

                <div className="col-12 col-sm-6 col-md-6 col-lg-6 mb4 ">
                <h6 >Genericos de Cruz Verde</h6>
                    <table className = "table table-striped card card-body">
                    <thead >
                        <tr>
                            <th>Generico </th>
                            <th>Precio </th>
                            
                        </tr>
                    </thead>
                    <tbody>
                    {genericosCV.map(genericoCV => (
                        <tr key = {genericoCV.medicamento }>
                            <td> {genericoCV.medicamento} </td>
                            <td> {genericoCV.precio} </td>

                        </tr>
                    ))}
                    </tbody>
                    </table>
                </div>
                
                <div className="col-12 col-sm-6 col-md-6 col-lg-6 mb4 ">
                <h6 >Medicamentos de Locatel</h6>
                    <table className = "table table-striped card card-body">
                    <thead >
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

                <div className="col-12 col-sm-6 col-md-6 col-lg-6 mb4 ">
                <h6 >Genericos de Locatel</h6>
                    <table className = "table table-striped card card-body">
                    <thead >
                        <tr>
                            <th>Generico </th>
                            <th>Precio </th>
                            
                        </tr>
                    </thead>
                    <tbody>
                    {genericosLC.map(genericoLC => (
                        <tr key = {genericoLC.medicamento }>
                            <td> {genericoLC.medicamento} </td>
                            <td> {genericoLC.precio} </td>

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

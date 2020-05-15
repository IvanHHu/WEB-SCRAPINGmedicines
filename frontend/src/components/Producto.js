import React from 'react';

const Producto = (props) => {

    const { medicamento, precio } = props.medicine;

    return(
         <div className="col-md-10"> 
            <table className = "table table-striped">
                <thead >
                    <tr>

                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td> {medicamento} </td>
                        <td> {precio} </td>
                    </tr>
                </tbody>
            </table>
        </div>

    )

}

export default Producto;
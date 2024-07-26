import React from "react"

const LifterList = ({lifters, updateLifter, updateCallback}) => {
    const onDelete = async (id) => {
        try {
            const options = {
                method: "DELETE"
            }
            const response = await fetch(`http://127.0.0.1:5000/delete_lifter/${id}`, options)
            if (response.status === 200) {
                updateCallback()
            } else {
                console.error("Failed to delete")
            }
        } catch (error) {
            alert(error)
        }
    }
    return <div>
        <h2>Lifters</h2>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Weight</th>
                    <th>Metrics</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {lifters.map((lifter) => (
                    <tr key={lifter.id}>
                        <td>{lifter.name}</td>
                        <td>{lifter.weight}</td>
                        <td>{lifter.positionalPoints.map((point, index) => (
                            <div key={index}>{point.points}</div>
                            ))}
                        </td>
                        <td>{lifter.positionalPoints.map((point, index) => (
                            <div key={index}>{point.distances}</div>
                            ))}
                        </td>
                        <td>
                            <button onClick={() => updateLifter(lifter)}>Update</button>
                            <button onClick={() => onDelete(lifter.id)}>Delete</button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}

export default LifterList

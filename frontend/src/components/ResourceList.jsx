import React from "react"

const ResourceList = ({resources, updateResource, updateCallback}) => {
    const onDelete = async (id) => {
        try {
            const options = {
                method: "DELETE"
            }
            const response = await fetch(`http://127.0.0.1:5000/delete_resource/${id}`, options)
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
        <h2>Resources</h2>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Program</th>
                    <th>Videos</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {resources.map((resource) => (
                    <tr key={resource.id}>
                        <td>{resource.name}</td>
                        <td>{resource.program}</td>
                        <td>{resource.links.map((link, index) => (
                            <div key={index}>{link.link}</div>
                            ))}
                        </td>
                        <td>
                            <button onClick={() => updateResource(resource)}>Update</button>
                            <button onClick={() => onDelete(resource.id)}>Delete</button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}

export default ResourceList

import {useState} from "react"

const LifterForm = ({ existingLifter = {}, updateCallback}) => {
    const [name, setName] = useState(existingLifter.name || "")
    const [weight, setWeight] = useState(existingLifter.weight || "")
    const [positionalPoints, setPositionalPoints] = useState(null)

    const updating = Object.entries(existingLifter).length !== 0

    const onSubmit = async (e) => {
        e.preventDefault()

        const formData = new FormData();
        formData.append('name', name);
        formData.append('weight', weight);
        if (positionalPoints) {
            formData.append('positionalPoints', positionalPoints);
        }
        
        const url = "http://127.0.0.1:5000/" + (updating ? `update_lifter/${existingLifter.id}` : "create_lifter")
        const options = {
            method: updating ? "PATCH" : "POST",
            body: formData
        }
        const response = await fetch(url, options)
        if (response.status !== 201 && response.status !== 200) {
            const data = await response.json()
            alert(data.message)
        } else {
            updateCallback()
        }
    }

    const removeMetrics = async (id) => {
        try {
            const options = {
                method: "DELETE"
            }
            const response = await fetch(`http://127.0.0.1:5000/delete_metrics/${id}`, options)
            if (response.status === 200) {
                updateCallback()
            } else {
                console.error("Failed to delete")
            }
        } catch (error) {
            alert(error)
        }
    }

    return (
        <form onSubmit={onSubmit}>
            <div>
                <label htmlFor="name">Name:</label>
                <input 
                    type="text" 
                    id="name" 
                    value={name} 
                    onChange={(e) => setName(e.target.value)} 
                />
            </div>
            <div>
                <label htmlFor="weight">Weight:</label>
                <input 
                    type="text" 
                    id="weight" 
                    value={weight} 
                    onChange={(e) => setWeight(e.target.value)} 
                />
            </div>
            <div>
                <label htmlFor="positionalPoints">Picture: </label>
                <input 
                    type="file" 
                    id="positionalPoints" 
                    onChange={(e) => setPositionalPoints(e.target.files[0])} 
                />
                <button type="button" onClick={() => removeMetrics(existingLifter.id)}>Remove All Metrics</button>
            </div>
            <button type="submit">{updating ? "Update Lifter" : "Create New Lifter"}</button>
        </form>
    );
}

export default LifterForm

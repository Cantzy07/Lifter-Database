import {useState} from "react"

const ResourceForm = ({ existingResource = {}, updateCallback}) => {
    const [name, setName] = useState(existingResource.name || "")
    const [program, setProgram] = useState(existingResource.program || "")
    const [links, setLinks] = useState(existingResource.links || [""])

    const updating = Object.entries(existingResource).length !== 0

    const onSubmit = async (e) => {
        e.preventDefault()

        const formData = new FormData();
        formData.append('name', name);
        formData.append('program', program);
        links.forEach((link, index) => {
            formData.append(`links[${index}]`, link);
        })
        
        const url = "http://127.0.0.1:5000/" + (updating ? `update_resource/${existingResource.id}` : "create_resource")
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

    const removeLinks = async (id) => {
        try {
            const options = {
                method: "DELETE"
            }
            const response = await fetch(`http://127.0.0.1:5000/delete_links/${id}`, options)
            if (response.status === 200) {
                updateCallback()
            } else {
                console.error("Failed to delete")
            }
        } catch (error) {
            alert(error)
        }
    }

    const handleLinkChange = (e, index) => {
        const newLinks = [...links];
        newLinks[index] = e.target.value;
        setLinks(newLinks);
    };

    // Function to remove a specific link field
    const removeLinkField = (index) => {
        const newLinks = links.filter((_, i) => i !== index);
        setLinks(newLinks);
    };

    const addLinkField = () => {
        setLinks([...links, ""]);
    };

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
                <label htmlFor="weight">Program:</label>
                <input 
                    type="text" 
                    id="program" 
                    value={program} 
                    onChange={(e) => setProgram(e.target.value)} 
                />
            </div>
            <div>
                <label>Video Links:</label>
                {links.map((link, index) => (
                    <div key={index}>
                        <input 
                            type="text" 
                            value={link}
                            onChange={(e) => handleLinkChange(e, index)} 
                        />
                        <button type="button" onClick={() => removeLinkField(index)}>Remove</button>
                    </div>
                ))}
                <button type="button" onClick={addLinkField}>Add Another Link</button>
            </div>
            <button type="submit">{updating ? "Update Resource" : "Create New Resource"}</button>
            {updating && (
                <button type="button" onClick={() => removeLinks(existingResource.id)}>Remove All Links</button>
            )}
        </form>
    );
}

export default ResourceForm

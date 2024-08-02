import Reach, { useState } from 'react';

const MatchingButton = () => {
    const [file, setFile] = useState(null);
    const [weight, setWeight] = useState('')
    const [matchingData, setMatchingData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0])
    }

    const findMatching = async () => {
        if (!file) {
            alert("Please upload a picture first")
            return
        }

        try {
            setLoading(true)
            setError(null)

            const formData = new FormData()
            formData.append("file", file)
            formData.append("weight", weight)

            const options = {
                method: "POST",
                body: formData,
            }
            const response = await fetch(`http://127.0.0.1:5000/find_matching`, options)
            if (response.status === 200) {
                const data = await response.json()
                setMatchingData(data)
            } else {
                console.error("Failed to delete")
            }
        } catch (error) {
            setError(error.message)
            alert(error)
        } finally {
            setLoading(false)
        }
    }

    return (
            <div>
                <label htmlFor="weight">Weight:</label>
                <input 
                    type="text" 
                    id="weight" 
                    value={weight} 
                    onChange={(e) => setWeight(e.target.value)} 
                />
                <label htmlFor="positionalPoints">Picture:</label>
                <input 
                    type="file" 
                    id="positionalPoints" 
                    onChange={handleFileChange} 
                />
                <button type="button" onClick={() => findMatching()}>Find Matching Lifter</button>
                {loading && <div>Loading...</div>}
                {error && <div>Error: {error}</div>}
                {matchingData && (
                    <div>
                        <h2>Matching Lifter:</h2>
                        <pre>{JSON.stringify(matchingData, null, 2)}</pre>
                    </div>
                )}
            </div>
    )
}

export default MatchingButton

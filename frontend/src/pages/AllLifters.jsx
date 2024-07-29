import { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import LifterList from '../components/LifterList'
import '../App.css';
import LifterForm from '../components/LifterForm';

function AllLifters() {
    const [lifters, setLifters] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false)
    const[currentLifter, setCurrentLifter] = useState({})

    useEffect(() => {
      fetchLifters()
    }, []);

    const fetchLifters = async () => {
      const response = await fetch("http://127.0.0.1:5000/lifters");
      const data = await response.json();
      setLifters(data.lifters);
      console.log(data.lifters);
    };

    const closeModal = () => {
      setIsModalOpen(false)
      setCurrentLifter({})
    }

    const openCreateModal = () => {
      if (!isModalOpen) setIsModalOpen(true)
    }

    const openEditModal = (lifter) => {
      if (isModalOpen) return
      setCurrentLifter(lifter)
      setIsModalOpen(true)
    }

    const onUpdate = () => {
      closeModal()
      fetchLifters()
    }

  return (
    <>
      <Navbar />
      <LifterList lifters={lifters} updateLifter={openEditModal} updateCallback={onUpdate}/>
      <button onClick={openCreateModal}>Create New Lifter</button>
      { isModalOpen && <div className="modal">
        <div className="modal-content">
          <span className="close" onClick={closeModal}>&times;</span>
          <LifterForm existingLifter={currentLifter} updateCallback={onUpdate}/>
        </div>
      </div>

      }
      
    </>
  );
}

export default AllLifters

import Header from '../components/Header';
import MatchingButton from '../components/MatchingButton';
import Navbar from '../components/Navbar';


export default function MatchingLifter(){
    return (
        <>
            <Navbar />
            <Header />
            <h2>Compare Metrics such as weight and joint length to find the most similar powerlifter</h2>
            <MatchingButton />
        </>
    )
}
export default function Navbar() {
    return (
         <nav className="nav">
            <a href="/" className="site-title">
                Lifter Database
            </a>
            <ul>
                <li>
                    <a href="/MatchingLifter">Matching Lifter</a>
                </li>
                <li>
                    <a href="/AllLifters">All Lifters</a>
                </li>
                <li>
                    <a href="/Resources">Resources</a>
                </li>
            </ul>
        </nav>
    ) 
}
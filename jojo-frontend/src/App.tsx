import "./App.css";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
// import Test from "./pages/Test";

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={ <Home/>} />
        {/* <Route path="/test" element={<Test/>}/> */}
        {/* Other routes */}
      </Routes>
    </Router>
  );
}

export default App;

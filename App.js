import './App.css';
import React, {useState, useEffect} from 'react'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'

function App() {

  const [infolist, setInfolist] = useState([{}])

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [email, setEmail] = useState('')

  // //read all info
  // useEffect(()=>{
  //   axios.get('http://localhost:8000/api/UserInfo')
  //     .then(res => {
  //       setInfolist(res.data)
  //     })
  // });

  //post todo
  const addInfo = () => {
    axios.post('http://localhost:8000/api/UserInfo/', {'username': username, 'password': password, 'email':email})
      .then(res=>console.log(res))
  };

  return (
      <div className="App list-group-item justify-content-center align-items-center mx-auto"
          style={{"width":"400px", "backgroundColor":"white", "marginTop":"15px"}}>
            <h1 className='card text-white bg-primary mb-1' styleName="max-width:20rem;">Task Manager</h1>
            <h6 className='card text-white bg-primary mb-3' styleName="max-width:20rem;">FastAPI React MongoDB</h6>
            <h5 className='card text-white bg-dark mb-3' styleName="max-width:20rem;">Add your info</h5>
            <span className='card-text'>
              <input className='mb-2 form-control usernameIn' onChange={Event => setUsername(Event.target.value)} placeholder='Username'/>
              <input className='mb-2 form-control passwordIn' onChange={Event => setPassword(Event.target.value)} placeholder='Password'/>
              <input className='mb-2 form-control emailIn' onChange={Event => setEmail(Event.target.value)} placeholder='Email'/>
              <button className='btn btn-outline-primary mx-2 mb-3' onClick ={addInfo} style={{'borderRadius':'50px', 'font-weight':'bold'}}>Add info</button>
            </span>
            <h5 className='card text-white bg-dark mb-3'>your info</h5>
            <div>
              {/* item -extern*/}
            </div>
            <h6 className='card text-dark bg-warning py-1 mb-0'>copyright</h6>
      </div>
  );
}

export default App;

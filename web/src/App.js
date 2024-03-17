import './App.css';

import { ModelViewport } from './components/ModelViewport';


function App() {
  return (
    <div className="App"  >
      <div className='form bg-black'>
        {/* <Form /> */}
        <h1 className="text-3xl font-bold underline bg-red-400">
          Hello world!
        </h1>
      </div>
      <ModelViewport />
    </div>
  );
}

export default App;
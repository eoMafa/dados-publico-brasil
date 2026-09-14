import IndicadorCard from "./components/IndicadorCard";
import BuscaCnpj from "./components/BuscaCnpj";
import BuscaCep from "./components/BuscaCep";
import BuscaFeriado from "./components/BuscaFeriado";


function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dados Públicos Brasil</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <IndicadorCard endpoint="selic" titulo="SELIC" cor="#2563eb" />
        <IndicadorCard endpoint="ipca" titulo="IPCA" cor="#16a34a" />
        <IndicadorCard endpoint="dolar" titulo="Dólar" cor="#9333ea" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <BuscaCnpj />
        <BuscaCep />
        <BuscaFeriado />
      </div>
    </div>
  );
}

export default App;
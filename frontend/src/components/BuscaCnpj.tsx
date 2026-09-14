import {useState} from "react";

interface Empresa {
    razao_social: string | null;
    nome_fantasia: string | null;
    situacao_cadastral: string | null;
    municipio: string | null;
    uf: string | null;
    atividade_principal: string | null;
    codigo_atividade_principal: string | null;
}

function BuscaCnpj() {
    const [cnpj, setCnpj] = useState("");
    const [empresa, setEmpresa] = useState<Empresa | null>(null);
    const [carregando, setCarregando] = useState(false);
    const [erro, setErro] = useState<string | null>(null);

    function buscarCnpj() {
        setCarregando(true);
        setErro(null);
        setEmpresa(null);

        fetch(`${import.meta.env.VITE_API_URL}/cnpj/${cnpj}`)
            .then((resposta) => {
                if(!resposta.ok) {
                    throw new Error("CNPJ inválido ou não encontrado");
                }
                return resposta.json();
            })
            .then((dados) => setEmpresa(dados))
            .catch((erro) => setErro(erro.message))
            .finally(() => setCarregando(false));
    }

    return (
        <div className="bg-white rounded-lg shadow p-4">
            <h2 className="text-lg font-semibold text-gray-800 mb-3">Buscar CNPJ</h2>
            <div className="flex gap-2">
                <input
                    type="text"
                    value={cnpj}
                    onChange={(evento) => setCnpj(evento.target.value)}
                    placeholder="Digite o CNPJ (só números)"
                    className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
                />
                <button onClick={buscarCnpj} className="bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-blue-700">Buscar</button>
            </div>
            
            {carregando && <p className="text-gray-500 text-sm mt-3">Carregando...</p>}
            {erro && <p className="text-red-500 text-sm mt-3">Erro: {erro}</p>}
            {empresa && (
                <p className="text-gray-700 text-sm mt-3">{empresa.razao_social}</p>
            )}
        </div>
    );
}

export default BuscaCnpj;
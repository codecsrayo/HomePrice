import { createSignal, onMount } from 'solid-js';


const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', currencyDisplay: 'code' }).format(value);
}


export default function Historical() {
    const [data, setData] = createSignal({});

    onMount(() => {
        const storedData = window.localStorage.getItem("data");
        if (storedData) {
            setData(JSON.parse(storedData));
        }

      
        
    });

    


    return (
        <div class="flex flex-col items-center mt-10 space-y-4 p-6 bg-gray-100 rounded-lg shadow-lg max-w-lg mx-auto h-[80vh]  overflow-auto">
            <h2 class="text-xl font-bold text-gray-800 mb-4">Información de la Propiedad</h2>
            <div class="flex flex-col w-full">
                <div class="flex items-center">
                    <p class="font-semibold text-gray-600">Dirección:</p>
                </div>
                <p>{data()?.address || 'N/A'}</p>

                <div class="flex items-center">
                    <p class="font-semibold text-gray-600">Ciudad:</p>
                </div>
                <p>{data()?.city || 'N/A'}</p>

                <div class="flex items-center">
                    <p class="font-semibold text-gray-600">Estado:</p>
                </div>
                <p>{data()?.state || 'N/A'}</p>

                <div class="flex items-center">
                    <p class="font-semibold text-gray-600">Código Postal:</p>
                </div>
                <p>{data()?.zip_code || 'N/A'}</p>

                <div class="flex items-center">
                    <p class="font-semibold text-gray-600">Habitaciones:</p>
                </div>
                <p>{data()?.bedrooms || 'N/A'}</p>

                <div class="flex items-center">
                    <p class="font-semibold text-gray-600">Baños:</p>
                </div>
                <p>{data()?.bathrooms || 'N/A'}</p>

                <div class="flex items-center">
                    <p class="font-semibold text-gray-600">Metros Cuadrados:</p>
                </div>
                <p>{data()?.square_feet || 'N/A'}</p>

                <div class="flex items-center">
                    <p class="font-semibold text-gray-600">Tamaño del Lote:</p>
                </div>
                <p>{data()?.lot_size || 'N/A'}</p>

                <div class="flex items-center">
                    <p class="font-semibold text-gray-600">Año de Construcción:</p>
                </div>
                <p>{data()?.year_built || 'N/A'}</p>

                <div class="flex items-center">
                    <p class="font-semibold text-gray-600">Tipo de Propiedad:</p>
                </div>
                <p>{data()?.property_type || 'N/A'}</p>

                <div class="flex items-center">
                    <p class="font-semibold text-gray-600">Precio:</p>
                </div>
                <p>{formatCurrency(data()?.price) || 'N/A'}</p>

                <div class="flex items-center">
                    <p class="font-semibold text-green-600">Precio Predicción:</p>
                </div>
                <p>{formatCurrency(data()?.predicted_price) || 'N/A'}</p>

                <div class="flex items-center">
                    <span class="material-icons text-gray-500 mr-2">schedule</span>
                    <p class="font-semibold text-gray-600">Fecha de Predicción:</p>
                </div>
                <p>{String(data()?.prediction_date).substring(0,10) || 'N/A'}</p>
            </div>
        </div>
    );
}

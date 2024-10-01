import { createSignal, For } from 'solid-js';



const formFields = [
  { label: "Dirección", type: "text", placeholder: "CARRERA 43b#43-45" },
  { label: "Municipio", type: "text", placeholder: "ANTIOQUÍA" },
  { label: "Ciudad", type: "text", placeholder: "MEDELLÍN" },
  { label: "Código Zip", type: "text", placeholder: "05007" },
  { label: "Baños", type: "number", placeholder: "6" },
  { label: "Habitaciones", type: "number", placeholder: "6" },
  { label: "Metros cuadrados", type: "number", placeholder: "200" },
  { label: "Tamaño del lote", type: "number", placeholder: "400" },
  { label: "Año de construcción", type: "number", placeholder: "2024" },
  { label: "Categoría", type: "text", placeholder: "FAMILIAR" },
];

const FormComponent = () => {
  const [formValues, setFormValues] = createSignal({});

  const handleSubmit = (e) => {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const values = Object.fromEntries(formData.entries());
    setFormValues(values);
    console.log("Formulario enviado:", values);

    // Aquí puedes agregar la lógica para enviar los datos al servidor
    // Por ejemplo, usando fetch:
    /*
    fetch(import.meta.env.PUBLIC_API + '/api/v1/predict/history', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(values),
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
    */
  };

  return (
    <form onSubmit={handleSubmit} class="border border-white p-4 h-[500px] overflow-y-auto">
      <h2 class="text-white text-sm uppercase">Anuncia tu propiedad</h2>
      <p class="text-white italic text-xs mt-5 mb-4">
        Ingresa los detalles a continuación para averiguar el valor de tu propiedad.
      </p>
      <div class="flex flex-wrap -mx-2">
        <For each={formFields}>
          {(field, index) => (
            <div
              class={`w-1/2 px-2 mb-4 ${index() % 2 === 0 ? 'pr-2' : 'pl-2'}`}
            >
              <label for={field.label} class="block text-left text-xs uppercase mb-1 text-white">
                {field.label}
              </label>
              <input
                class="w-full h-8 px-2 bg-gray-300 rounded"
                type={field.type}
                id={field.label}
                name={field.label}
                placeholder={field.placeholder}
                required
              />
            </div>
          )}
        </For>
      </div>
      <button
        type="submit"
        class="mt-5 px-4 py-2 bg-orange-600 text-white rounded hover:opacity-80 text-xs uppercase"
      >
        Consultar
      </button>
    </form>
  );
};

export default FormComponent;
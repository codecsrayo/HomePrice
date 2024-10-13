import { createMutation, useQueryClient } from "@tanstack/solid-query";
import { createSignal } from "solid-js";

type PropertyFormData = {
    address: string;
    city: string;
    state: string;
    zip_code: string;
    bedrooms: number;
    bathrooms: number;
    square_feet: number;
    lot_size: number;
    year_built: number;
    property_type: string;
    price: number;
};

const PropertyForm = (props:{ setId:(cardId: string)=>void }) => {
    const queryClient = useQueryClient();
    const [formData, setFormData] = createSignal<PropertyFormData>({
        address: "",
        city: "",
        state: "",
        zip_code: "",
        bedrooms: 0,
        bathrooms: 0,
        square_feet: 0,
        lot_size: 0,
        year_built: 0,
        property_type: "",
        price: 0,
    });

    const submitMutation = createMutation(() => ({
        mutationFn: async (newPropertyData: PropertyFormData) => {
            const response = await fetch(`${import.meta.env.PUBLIC_API}/v1/predict`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(newPropertyData),
            });
            if (!response.ok) throw new Error("Error al enviar los datos");
            return response.json();

        },
        onSuccess: (data)=>{
            queryClient.invalidateQueries({queryKey:["chats"]})
            props.setId(data?.id)

        }
    }));

    const handleSubmit = (e: Event) => {
        e.preventDefault();
        submitMutation.mutate(formData());
    };

    const handleInputChange = (e: Event) => {
        const { name, value } = e.target as HTMLInputElement;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const inputField = (label: string, name: keyof PropertyFormData, type: string) => (
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{label}</label>
            <input
                type={type}
                name={name}
                value={formData()[name]}
                onInput={handleInputChange}
                class="mt-1 text-black block w-full px-3 py-2 bg-white border border-gray-300 rounded-md text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary disabled:bg-gray-100 disabled:text-gray-500 disabled:border-gray-200 transition duration-150 ease-in-out"
                required
            />
        </div>
    );

    return (
        <div class="bg-white shadow-md rounded-lg max-w-2xl mx-auto p-8 h-fit mt-10 max-h-[90vh] overflow-auto border border-slate-300">
            <h2 class="text-2xl font-bold mb-6 text-center text-gray-800 uppercase">Property Details</h2>
            <form onSubmit={handleSubmit} class="space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {inputField("Address", "address", "text")}
                    {inputField("City", "city", "text")}
                    {inputField("State", "state", "text")}
                    {inputField("Zip Code", "zip_code", "text")}
                    {inputField("Bedrooms", "bedrooms", "number")}
                    {inputField("Bathrooms", "bathrooms", "number")}
                    {inputField("Square Feet", "square_feet", "number")}
                    {inputField("Lot Size", "lot_size", "number")}
                    {inputField("Year Built", "year_built", "number")}
                    {inputField("Property Type", "property_type", "text")}
                    {inputField("Price", "price", "number")}
                </div>
                <div class="mt-6">
                    <button
                        type="submit"
                        class={`w-full bg-[#ff5f2e] text-white py-2 px-4 rounded-md hover:bg-[#ff5f2e]/90 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition duration-150 ease-in-out ${submitMutation.isPending ? "opacity-50 cursor-not-allowed" : ""
                            }`}
                        disabled={submitMutation.isPending}
                    >
                        {submitMutation.isPending ? "Loading..." : "Send"}
                    </button>
                </div>
                {submitMutation.isError && <p class="text-red-600 mt-2">Error to send.</p>}
                {submitMutation.isSuccess && <p class="text-green-600 mt-2">Data send.</p>}
            </form>
        </div>
    );
};

export default PropertyForm;
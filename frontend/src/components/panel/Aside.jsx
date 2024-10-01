
export default function Sidebar({ data }) {

  
    const handleClick = (item) => {
        const $historical = document.querySelector(".historical");
        const $form = document.querySelector("form");

        if ($form && $historical) {
            $form.style.visibility = "hidden";
            $historical.style.visibility = "visible";
            
        }

        window.localStorage.setItem('data', JSON.stringify(item))



    };

    return (
        <>
            <aside class="page-leftbar">
                <div class="space-y-2 m-2">
                    {data && data?.map((item) => (
                        <button
                            id="btn-chat"
                            class="text-sm text-start space-y-2 bg-gray-600 px-2 rounded-sm w-full hover:opacity-90 h-8 text-white"
                            title={item.address}
                            onClick={() => {
                                handleClick(item)


                            }

                            }
                        >
                            {item.address}
                        </button>
                    ))}
                </div>
            </aside>

        </>

    );
}


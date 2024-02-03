using Base: iterate

struct VerboseIterable{T}
    iterable::T
    verbose::Bool
    starting_msg::String
    python_iterator::Bool
end

function VerboseIterator(iterable, verbose, starting_msg="Starting iteration...", python_iterator=false)
    VerboseIterable(iterable, verbose, starting_msg, python_iterator)
end

function Base.iterate(vi::VerboseIterable, state=(1, time(), 0, 0, false))  # Initial state
    iterable, verbose = vi.iterable, vi.verbose
    idx, start_time, counter, dispcnt, first_item_completed = state
    total_length = length(iterable)

    if !first_item_completed
        if verbose
            println(vi.starting_msg)
        end
        if vi.python_iterator
            idx = 0  # Python iterators start at 0
        end
        first_item_completed = true
    end

    if idx > total_length || (vi.python_iterator && idx == total_length)
        if verbose
            elapsed = round(time() - start_time, digits=2)
            println("\r100% ($counter) completed in $(elapsed)s")
        end
        return nothing  # Iteration is complete
    end

    item = iterable[idx]
    idx += 1

    update_verbose_iterator_display(counter, total_length, start_time, dispcnt, verbose)

    return (item, (idx, start_time, counter, dispcnt, first_item_completed))
end

@inline update_verbose_iterator_display(counter, total_length, start_time, dispcnt, verbose) = begin
    counter += 1
    dispcnt += 1

    if verbose && dispcnt >= 1000
        percent = round(Int, 100 * counter / total_length)
        elapsed_time = round(time() - start_time, digits=2)
        print("\r$(percent)% ($counter) completed in $(elapsed_time)s")
        dispcnt = 0  # Reset display counter
    end
end
using Base: iterate

struct VerboseIterable{T}
    iterable::T
    verbose::Bool
    starting_msg::String
    python_iterator::Bool
    update_frequency::Int
end

"""
A wrapper around an iteraterable which prints the progress of the iteration.
If the iteration exceeds the max allowable time, the iteration will be stopped.

Args:
    iterable::T                  The iterable to iterate over
    verbose::Bool                 Whether to print the progress of the function
    starting_msg::String          Message to print when starting the iteration
    python_iterator::Bool         Whether the iterator is a python iterator (starts at 0)

Raises:
    ValueError: if an unsupported gate is encountered

Returns:
    VerboseIterable: The iterable wrapped in a VerboseIterable
"""
function VerboseIterator(iterable, verbose, starting_msg="Starting iteration...", python_iterator=false, update_frequency=1000)
    VerboseIterable(iterable, verbose, starting_msg, python_iterator, update_frequency)
end

function Base.iterate(vi::VerboseIterable, state=(1, time(), 0, 0, false))  # Initial state
    iterable, verbose, update_frequency = vi.iterable, vi.verbose, vi.update_frequency
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
    counter += 1
    dispcnt += 1

    if verbose && dispcnt >= update_frequency
        percent = round(Int, 100 * counter / total_length)
        elapsed_time = round(time() - start_time, digits=2)
        print("\r$(percent)% ($counter) completed in $(elapsed_time)s")
        dispcnt = 0  # Reset display counter
    end

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